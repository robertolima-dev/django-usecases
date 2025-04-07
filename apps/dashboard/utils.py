from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model

from apps.book.models import Book
from apps.course.models import Course
from apps.report.models import ReportRequest

User = get_user_model()


def send_dashboard_data():
    data = {
        "type": "dashboard_data",
        "users_count": User.objects.count(),
        "courses_count": Course.objects.count(),
        "reports_count": ReportRequest.objects.count(),
        "books_count": Book.objects.count(),
    }

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "dashboard",
        {
            "type": "send_dashboard_update",
            "data": data
        }
    )
