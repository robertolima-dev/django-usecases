# from django.db.models import Q
from django.utils.dateparse import parse_date
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.book.models import Book
from apps.course.models import Course
from apps.notifications.models import Notification
from apps.throttle.models import UserQuota


@extend_schema(
    tags=["Dashboard"]
)
class DashboardAPIView(APIView):
    def get(self, request):
        date_from_str = request.GET.get("date_from")
        date_to_str = request.GET.get("date_to")
        date_from = parse_date(date_from_str) if date_from_str else None
        date_to = parse_date(date_to_str) if date_to_str else None

        user_id = request.GET.get("user_id")
        action_type = request.GET.get("action_type")

        date_filter = {}
        if date_from and date_to:
            date_filter["created_at__range"] = (date_from, date_to)

        data = {}

        if not action_type or action_type == "course":
            data["courses"] = Course.objects.filter(**date_filter).count()

        if not action_type or action_type == "upload":
            upload_filter = {**date_filter}
            if user_id:
                upload_filter["user_id"] = user_id
            data["uploads"] = UserQuota.objects.filter(action="upload", **upload_filter).count()  # noqa: E501

        if not action_type or action_type == "book":
            book_filter = {**date_filter}
            if user_id:
                book_filter["author_id"] = user_id
            data["books"] = Book.objects.filter(**book_filter).count()  # noqa: E501

        if not action_type or action_type == "notification":
            notif_filter = {**date_filter}
            if user_id:
                notif_filter["obj_id"] = user_id
            data["notifications"] = Notification.objects.filter(**notif_filter).count()  # noqa: E501

        return Response(data)
  # noqa: E501