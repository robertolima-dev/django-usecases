# course/views.py
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model
from django.db.models import Avg, Count, Q
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (OpenApiExample, OpenApiParameter,
                                   OpenApiResponse, extend_schema)
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.course.filters import CourseFilter
from apps.course.models import Course
from apps.dashboard.events import send_admin_event
from apps.dashboard.utils import send_dashboard_data
from apps.notifications.models import Notification

from .serializers import CourseSerializer

# from django.contrib.postgres.search import SearchVector


User = get_user_model()


@extend_schema(
    tags=["Courses"]
)
class CourseViewSet(ModelViewSet):
    queryset = Course.objects.select_related("category", "instructor__user").prefetch_related("tags") # noqa501
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = CourseFilter
    search_fields = ["title", "description"]
    ordering_fields = ["price", "workload", "start_date", "created_at", "avg_rating", "paid_count",] # noqa501
    ordering = ["-created_at", "-avg_rating"]

    @swagger_auto_schema(
        operation_description="Endpoint customizado para retornar cursos ativos", # noqa501
        responses={200: CourseSerializer(many=True)},
    )
    @action(detail=False, methods=["get"], url_path="actives")
    def active_courses(self, request):
        courses = Course.objects.filter(is_active=True)
        serializer = self.get_serializer(courses, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Listar cursos gratuitos",
        description="Retorna todos os cursos gratuitos disponíveis na plataforma.", # noqa501
        responses={
            200: OpenApiResponse(
                response=CourseSerializer(many=True),
                description="Lista de cursos com `is_free=True`"
            )
        },
        parameters=[
            OpenApiParameter(
                name="ordering",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Campo para ordenação. Ex: `ordering=-created_at`"
            ),
        ],
        examples=[
            OpenApiExample(
                name="Exemplo de resposta",
                value=[
                    {
                        "id": 1,
                        "title": "Curso Django Básico",
                        "description": "Aprenda o básico de Django",
                        "is_free": True,
                        "price": "0.00",
                        "category": {"id": 1, "name": "Tecnologia"},
                        "instructor": {"id": 2, "user": "prof@curso.com", "bio": "Dev backend"}, # noqa501
                        "tags": [{"id": 1, "name": "python"}],
                        "created_at": "2025-04-15T12:34:56Z",
                    }
                ],
                response_only=True
            )
        ],
        tags=["Courses"],
    )
    @action(detail=False, methods=["get"], url_path="free")
    def free_courses(self, request):
        courses = Course.objects.filter(is_free=True)
        serializer = self.get_serializer(courses, many=True)
        return Response(serializer.data)

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
