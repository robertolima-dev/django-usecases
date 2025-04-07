from django.db.models import Count
from django_filters.rest_framework import (CharFilter, DjangoFilterBackend,
                                           FilterSet, NumberFilter)
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from apps.book.api.book.serializers import BookSerializer
from apps.book.models import Book


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
        serializer.save(author=self.request.user)
