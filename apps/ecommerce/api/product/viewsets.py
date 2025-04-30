import os

from django.conf import settings
from django.db.models import Q as Qdjango
from drf_spectacular.utils import extend_schema
from elasticsearch_dsl.query import Q  # type: ignore
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from apps.ecommerce.api.product.serializers import (
    ProductCustomSerializer,
    ProductSerializer,
)
from apps.ecommerce.documents import ProductDocument
from apps.ecommerce.models import Product
from common.elastisearch_pagination import ElasticsearchLimitOffsetPagination

USE_ELASTIC = settings.PROJECT_ENV == "develop_local"


@extend_schema(
    tags=["E-commerce"]
)
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if USE_ELASTIC and self.action == "list":
            return ProductCustomSerializer
        return ProductSerializer

    def get_pagination_class(self):
        if USE_ELASTIC and self.action == "list":
            return ElasticsearchLimitOffsetPagination
        return LimitOffsetPagination

    def list(self, request, *args, **kwargs):
        search_query = request.query_params.get("search")
        ordering = self.request.query_params.get("ordering")

        if USE_ELASTIC:

            s = ProductDocument.search()

            if search_query:
                match_name_or_description = Q("multi_match", query=search_query, fields=["name", "description"]) # noqa501
                active_filter = Q("term", is_active=True)
                composed_query = Q("bool", must=[match_name_or_description, active_filter]) # noqa501
                s = s.query(composed_query)
            else:
                s = s.query("term", is_active=True)

            if ordering:
                if ordering.startswith("-"):
                    s = s.sort({ordering[1:]: {"order": "desc"}})
                else:
                    s = s.sort(ordering)

            pages = self.paginate_queryset(s)

            if pages:
                hits_as_dicts = [hit.to_dict() for hit in pages]
                serializer = self.get_serializer(hits_as_dicts, many=True)
                return self.get_paginated_response(serializer.data)

            hits_as_dicts = [hit.to_dict() for hit in s.execute()]
            serializer = self.get_serializer(hits_as_dicts, many=True)
            return self.get_paginated_response(serializer.data)

        else:
            try:

                if not ordering:
                    ordering = '-created_at'

                f = Qdjango(is_active=True)

                if search_query:
                    f &= Qdjango(name__icontains=search_query) | Qdjango(description__icontains=search_query) # noqa501

                queryset = Product.objects.filter(f).order_by(ordering)

                page = self.paginate_queryset(queryset)
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            except Exception as e:
                return Response(
                    {'detail': str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.owner != self.request.user:
            raise PermissionDenied("Você não tem permissão para editar este produto.") # noqa501
        serializer.save()

    def perform_destroy(self, instance):
        if instance.owner != self.request.user:
            raise PermissionDenied("Você não tem permissão para excluir este produto.") # noqa501
        instance.delete()


@extend_schema(
    tags=["E-commerce"]
)
class ProductSearchAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        query = request.query_params.get("q", "").strip()

        if not query:
            return Response({"detail": "Parâmetro 'q' é obrigatório."}, status=400) # noqa501

        products = []

        if os.environ.get("PROJECT_ENV") == "develop_local":
            s = ProductDocument.search().query("multi_match", query=query, fields=["name", "description"]) # noqa501
            search_results = s.execute()

            ids = [hit.meta.id for hit in search_results]
            products = Product.objects.filter(id__in=ids)

        else:
            products = Product.objects.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
