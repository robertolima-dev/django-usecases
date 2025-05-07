from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


class MongoDBLimitOffsetPagination(LimitOffsetPagination):
    def paginate_queryset(self, queryset, request, view=None):
        """
        Paginador para consultas MongoDB usando pymongo.
        """
        self.limit = self.get_limit(request) or self.default_limit
        self.offset = self.get_offset(request)
        self.request = request

        self.count = queryset.collection.count_documents({})

        paginated_queryset = queryset.skip(self.offset).limit(self.limit)

        self.results = list(paginated_queryset)

        return self.results

    def get_paginated_response(self, data):
        """
        Formato de resposta similar ao DRF.
        """
        return Response({
            'count': self.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })
