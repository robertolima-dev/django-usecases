from rest_framework import status

# from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# from apps.analytics.filters import EventLogFilter
from apps.analytics.mongo_client import db
from common.pagination.mongodb_pagination import MongoDBLimitOffsetPagination


class EventLogView(APIView):
    pagination_class = MongoDBLimitOffsetPagination
    permission_classes = [IsAuthenticated]
    # filter_backends = [EventLogFilter, OrderingFilter]

    def post(self, request):
        event_data = {
            "event_type": request.data.get("event_type"),
            "description": request.data.get("description"),
            "timestamp": request.data.get("timestamp")
        }

        db.event_logs.insert_one(event_data)
        return Response({"message": "Evento registrado com sucesso!"}, status=status.HTTP_201_CREATED)  # noqa: E501

    def get(self, request):
        queryset = db.event_logs.find({}).sort("timestamp", -1)

        paginator = self.pagination_class()
        paginated_data = paginator.paginate_queryset(queryset, request)

        data = [
            {
                "event_type": item.get("event_type"),
                "description": item.get("description"),
                "timestamp": str(item.get("timestamp")),
            }
            for item in paginated_data
        ]

        return paginator.get_paginated_response(data)
