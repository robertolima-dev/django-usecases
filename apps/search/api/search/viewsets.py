from django.conf import settings
from elasticsearch import Elasticsearch
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apps.search.services.embedding_service import generate_embedding


class SemanticSearchViewSet(ViewSet):
    """
    ViewSet para busca híbrida (semântica + lexical) de livros.
    """

    def list(self, request):
        query = request.query_params.get("q")
        if not query:
            return Response({"detail": "Parâmetro 'q' é obrigatório."}, status=status.HTTP_400_BAD_REQUEST)  # noqa: E501

        query_vector = generate_embedding(query)

        es = Elasticsearch(
            hosts=[settings.ELASTICSEARCH_HOST],
            basic_auth=(settings.ELASTICSEARCH_USERNAME, settings.ELASTICSEARCH_PASSWORD),  # noqa: E501
            verify_certs=True
        )

        search_body = {
            "size": 10,
            "query": {
                "bool": {
                    "should": [
                        {
                            "script_score": {
                                "query": {"match_all": {}},
                                "script": {
                                    "source": "cosineSimilarity(params.query_vector, 'title_vector') + 1.0",  # noqa: E501
                                    "params": {
                                        "query_vector": query_vector
                                    }
                                }
                            }
                        },
                        {
                            "multi_match": {
                                "query": query,
                                "fields": ["title^2"],  # Boost no título
                                "type": "best_fields"
                            }
                        }
                    ],
                    "minimum_should_match": 1
                }
            }
        }

        response = es.search(index="semantic_books", body=search_body)

        results = [
            {
                "id": hit["_source"]["id"],
                "title": hit["_source"]["title"],
                "score": hit["_score"]
            }
            for hit in response["hits"]["hits"]
            if hit["_score"] >= 6
        ]

        return Response(results)
