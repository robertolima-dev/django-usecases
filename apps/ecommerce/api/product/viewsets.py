import os

from django.conf import settings
from django.db.models import Q
from elasticsearch import Elasticsearch
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from apps.ecommerce.api.product.serializers import ProductSerializer
from apps.ecommerce.documents import ProductDocument
from apps.ecommerce.models import Product

USE_ELASTIC = settings.PROJECT_ENV == "local"

if USE_ELASTIC:
    es = Elasticsearch(["http://localhost:9200"])


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        search_query = self.request.query_params.get("q")

        if USE_ELASTIC and search_query:

            res = es.search(
                index="products",
                query={
                    "multi_match": {
                        "query": search_query,
                        "fields": ["name", "description"]
                    }
                }
            )

            ids = [hit["_source"]["id"] for hit in res["hits"]["hits"]]
            return Product.objects.filter(id__in=ids)

        elif search_query:
            return Product.objects.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query)
            )

        return Product.objects.all()

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


class ProductSearchAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        query = request.query_params.get("q", "").strip()

        if not query:
            return Response({"detail": "Parâmetro 'q' é obrigatório."}, status=400) # noqa501

        products = []

        if os.environ.get("PROJECT_ENV") == "local":
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
