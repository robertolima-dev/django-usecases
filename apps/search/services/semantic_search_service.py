# from elasticsearch_dsl import Q

from apps.search.elasticsearch.semantic_documents import SemanticBookDocument


class SemanticSearchService:

    @staticmethod
    def search_semantic(query_embedding, top_k=10):
        """Faz busca semântica no Elasticsearch usando dense vectors."""
        s = SemanticBookDocument.search()
        s = s.query("script_score", script={
            "source": "cosineSimilarity(params.query_vector, 'title_vector') + 1.0",  # noqa: E501
            "params": {"query_vector": query_embedding}
        })
        s = s[:top_k]  # limita resultados
        return s.execute()
