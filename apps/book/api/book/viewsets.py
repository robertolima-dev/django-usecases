import hashlib

from django.core.cache import cache
from django.db.models import Count
from django.utils.decorators import method_decorator
from django_filters.rest_framework import (
    CharFilter,
    DjangoFilterBackend,
    FilterSet,
    NumberFilter,
)
from drf_spectacular.utils import extend_schema
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.book.api.book.serializers import BookSerializer
from apps.book.models import Book
from apps.dashboard.events import send_admin_event
from apps.dashboard.utils import send_dashboard_data
from common.decorators.logging import log_api_execution


class BookFilterSet(FilterSet):
    title = CharFilter(field_name="title", lookup_expr="icontains")
    author_id = NumberFilter(field_name="author_id")
    min_comments = NumberFilter(method="filter_min_comments")
    max_comments = NumberFilter(method="filter_max_comments")

    class Meta:
        model = Book
        fields = ["title", "author_id", "min_comments", "max_comments"]

    def filter_min_comments(self, queryset, name, value):
        return queryset.annotate(comments_count=Count("comments")).filter(comments_count__gte=value) # noqa501

    def filter_max_comments(self, queryset, name, value):
        return queryset.annotate(comments_count=Count("comments")).filter(comments_count__lte=value) # noqa501


@extend_schema(
    tags=["Books"]
)
@method_decorator(log_api_execution, name='dispatch')
class BookViewSet(ModelViewSet):
    serializer_class = BookSerializer
    queryset = Book.objects.select_related("author").prefetch_related("tags", "comments").annotate( # noqa501
        comments_count=Count("comments")
    )
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = BookFilterSet
    search_fields = ["title", "author__first_name", "author__last_name"]
    ordering_fields = ["title", "comments_count"]
    ordering = ["-comments_count"]

    def perform_create(self, serializer):
        book = serializer.save(author=self.request.user)

        self.clear_book_cache()

        send_dashboard_data()

        send_admin_event("book_created", {
            "id": book.id,
            "title": book.title,
            "author": book.author.username,
        })

    def perform_update(self, serializer):
        book = serializer.save()
        self.clear_book_cache(book_id=book.id)
        return book

    def perform_destroy(self, instance):
        self.clear_book_cache(book_id=instance.id)
        instance.delete()

    def retrieve(self, request, *args, **kwargs):
        book_id = self.kwargs.get('pk')
        cache_key = f"book_detail_{book_id}"

        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)

        instance = self.get_object()
        serializer = self.get_serializer(instance)

        cache.set(cache_key, serializer.data, timeout=3600)
        return Response(serializer.data)

    def generate_list_cache_key(self, request):
        """Gera uma cache_key única para cada combinação de parâmetros da listagem.""" # noqa501
        query_string = request.GET.urlencode()
        hashed_query = hashlib.md5(query_string.encode('utf-8')).hexdigest()
        return f"book_list_{hashed_query}"

    def list(self, request, *args, **kwargs):
        cache_key = self.generate_list_cache_key(request)
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)

        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data)
            cache.set(cache_key, paginated_response.data, timeout=3600)
            return paginated_response

        serializer = self.get_serializer(queryset, many=True)
        cache.set(cache_key, serializer.data, timeout=3600)
        return Response(serializer.data)

    def clear_book_cache(self, book_id=None):
        """Função para limpar caches de livros."""
        client = cache.client.get_client()
        backend = cache.client

        if book_id:
            cache.delete(f"book_detail_{book_id}")

        prefix = backend.make_key("")
        keys = client.keys(f"{prefix}book_list_*")

        if keys:
            client.delete(*keys)
