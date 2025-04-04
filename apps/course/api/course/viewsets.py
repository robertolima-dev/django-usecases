# course/views.py
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.viewsets import ModelViewSet

from apps.course.filters import CourseFilter
from apps.course.models import Course
from apps.notifications.models import Notification

from .serializers import CourseSerializer

User = get_user_model()


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.select_related("category", "instructor__user").prefetch_related("tags") # noqa501
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = CourseFilter
    search_fields = ["title", "description"]
    ordering_fields = ["price", "workload", "start_date", "created_at"]
    ordering = ["-created_at"]

    def perform_create(self, serializer):
        course = serializer.save()

        users = User.objects.all()
        for user in users:
            Notification.objects.create(
                user=user,
                title="Novo Curso Publicado!",
                message=f"{course.title} já está disponível."
            )

        channel_layer = get_channel_layer()
        for user in users:
            async_to_sync(channel_layer.group_send)(
                f"user_{user.id}",
                {
                    "type": "send_notification",
                    "title": "Novo Curso Publicado!",
                    "message": f"{course.title} já está disponível.",
                    "created_at": str(course.created_at)
                }
            )
