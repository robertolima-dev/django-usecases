from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


class ElasticsearchLimitOffsetPagination(LimitOffsetPagination):
    def paginate_queryset(self, queryset, request, view=None):
        self.limit = self.get_limit(request) or self.default_limit
        self.offset = self.get_offset(request)
        self.count = queryset.count()
        self.request = request
        return queryset[self.offset:self.offset + self.limit].execute()

    def get_paginated_response(self, data):
        return Response({
            'count': self.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })
