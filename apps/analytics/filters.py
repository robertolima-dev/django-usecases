from datetime import datetime

from rest_framework import filters


class EventLogFilter(filters.BaseFilterBackend):
    """
    Filtro para buscar logs de eventos no MongoDB.
    """

    def filter_queryset(self, request, queryset, view):
        event_type = request.query_params.get("event_type")
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")
        min_id = request.query_params.get("min_id")
        max_id = request.query_params.get("max_id")
        description = request.query_params.get("description")

        query = {}

        if event_type:
            query["event_type"] = event_type

        if description:
            query["description"] = {"$regex": description, "$options": "i"}

        if start_date:
            try:
                start_date = datetime.strptime(start_date, "%Y-%m-%d")
                query.setdefault("timestamp", {})["$gte"] = start_date
            except ValueError:
                pass

        if end_date:
            try:
                end_date = datetime.strptime(end_date, "%Y-%m-%d")
                query.setdefault("timestamp", {})["$lte"] = end_date
            except ValueError:
                pass

        if min_id:
            try:
                query["_id"] = {"$gte": int(min_id)}
            except ValueError:
                pass

        if max_id:
            try:
                if "_id" in query:
                    query["_id"]["$lte"] = int(max_id)
                else:
                    query["_id"] = {"$lte": int(max_id)}
            except ValueError:
                pass

        filtered_queryset = queryset.collection.find(query)

        return filtered_queryset
