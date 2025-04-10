# course/views.py
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model
# from django.contrib.postgres.search import SearchVector
from django.db.models import Avg, Count, Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.viewsets import ModelViewSet

from apps.course.filters import CourseFilter
from apps.course.models import Course
from apps.dashboard.events import send_admin_event
from apps.dashboard.utils import send_dashboard_data
from apps.notifications.models import Notification

from .serializers import CourseSerializer

User = get_user_model()


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.select_related("category", "instructor__user").prefetch_related("tags") # noqa501
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = CourseFilter
    search_fields = ["title", "description"]
    ordering_fields = ["price", "workload", "start_date", "created_at", "avg_rating", "paid_count",] # noqa501
    ordering = ["-created_at", "-avg_rating"]

    def get_queryset(self):

        # qs = Course.objects.annotate(
        #     search=SearchVector("title", "description")
        # )

        # q = self.request.query_params.get("q")
        # if q:
        #     qs = qs.filter(search=q)

        # return qs

        return Course.objects.annotate(
            avg_rating=Avg("ratings__rating"),
            paid_count=Count("payments", filter=Q(payments__status="paid"))
        )

    def perform_create(self, serializer):
        course = serializer.save()

        send_dashboard_data()

        send_admin_event("course_created", {
            "id": course.id,
            "title": course.title,
            "price": course.price,
            "created_at": str(course.created_at),
        })

        notification = Notification.objects.create(
            title="Novo Curso Publicado!",
            message=f"{course.title} já está disponível.",
            obj_code="platform",
            obj_id=None,
        )

        channel_layer = get_channel_layer()
        from django.contrib.auth import get_user_model
        User = get_user_model()
        for user in User.objects.all():
            async_to_sync(channel_layer.group_send)(
                f"user_{user.id}",
                {
                    "type": "send_notification",
                    "title": notification.title,
                    "message": notification.message,
                    "created_at": str(notification.created_at),
                    "obj_code": notification.obj_code,
                    "obj_id": notification.obj_id,
                }
            )
