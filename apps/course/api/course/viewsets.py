# from asgiref.sync import async_to_sync
# from channels.layers import get_channel_layer
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Avg, Count
from django.db.models import Q as Qdjango
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
)
from drf_yasg.utils import swagger_auto_schema
from elasticsearch_dsl.query import Q  # type: ignore
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.course.documents import CourseDocument
from apps.course.filters import CourseFilter
from apps.course.models import Course
from apps.course.tasks import notification_users_course
from apps.dashboard.events import send_admin_event
from apps.dashboard.utils import send_dashboard_data
from apps.notifications.models import Notification
from common.pagination.elastisearch_pagination import (  # noqa: E501
    ElasticsearchLimitOffsetPagination,
)

from .serializers import CourseSearchSerializer, CourseSerializer

USE_ELASTIC = settings.PROJECT_ENV == "develop_local"

# from django.contrib.postgres.search import SearchVector


User = get_user_model()


@extend_schema(
    tags=["Courses"]
)
class CourseViewSet(ModelViewSet):
    queryset = Course.objects.select_related("category", "instructor__user").prefetch_related("tags")  # noqa: E501
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = CourseFilter
    search_fields = ["title", "description"]
    ordering_fields = ["price", "workload", "start_date", "created_at", "avg_rating", "paid_count",]  # noqa: E501
    ordering = ["-created_at", "title", "price", ]

    def get_serializer_class(self):
        if USE_ELASTIC and self.action == "list":
            return CourseSearchSerializer
        return CourseSerializer

    def get_pagination_class(self):
        if USE_ELASTIC and self.action == "list":
            return ElasticsearchLimitOffsetPagination
        return LimitOffsetPagination

    @swagger_auto_schema(
        operation_description="Endpoint customizado para retornar cursos ativos",  # noqa: E501
        responses={200: CourseSerializer(many=True)},
    )
    @action(detail=False, methods=["get"], url_path="actives")
    def active_courses(self, request):
        courses = Course.objects.filter(is_active=True)
        serializer = self.get_serializer(courses, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Listar cursos gratuitos",
        description="Retorna todos os cursos gratuitos disponíveis na plataforma.",  # noqa: E501
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
                        "instructor": {"id": 2, "user": "prof@curso.com", "bio": "Dev backend"},  # noqa: E501
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

    def list(self, request, *args, **kwargs):

        ordering = request.query_params.get("ordering")
        search = request.query_params.get("search")
        title = request.query_params.get("title")
        description = request.query_params.get("description")
        ordering = request.query_params.get("ordering")

        if USE_ELASTIC:

            s = CourseDocument.search()
            filters = [Q("term", is_active=True)]

            # Filtros full-text aplicando boost
            if search:
                filters.append(Q(
                    "multi_match",
                    query=search,
                    fields=[
                        "title^3",
                        "description"
                    ],
                    operator="and"
                ))

            if title:
                # aplicado edge_ngram para auto complete
                filters.append(Q("match", title_autocomplete={"query": title, "operator": "and"}))  # noqa: E501

            if description:
                filters.append(Q("multi_match", query=description, fields=["description",]))  # noqa: E501

            # Filtros booleanos e por campo simples
            if is_free := request.query_params.get("is_free"):
                filters.append(Q("term", is_free=is_free.lower() == "true"))

            if category := request.query_params.get("category"):
                filters.append(Q("term", category__id=int(category)))

            # Filtro por tags (in múltiplos)
            tag_ids = request.query_params.getlist("tag_ids")
            if not tag_ids:
                tag_param = request.query_params.get("tag_ids")
                if tag_param:
                    tag_ids = tag_param.split(',')

            tag_ids = [int(t) for t in tag_ids if t.isdigit()]
            if tag_ids:
                tag_filters = [
                    Q("nested", path="tags", query=Q("term", **{"tags.id": tag}))  # noqa: E501
                    for tag in tag_ids
                ]
                filters.append(Q("bool", should=tag_filters, minimum_should_match=1))  # noqa: E501

            # Filtros numéricos
            if price_min := request.query_params.get("price_min"):
                filters.append(Q("range", price={"gte": float(price_min)}))

            if price_max := request.query_params.get("price_max"):
                filters.append(Q("range", price={"lte": float(price_max)}))

            if workload_min := request.query_params.get("workload_min"):
                filters.append(Q("range", workload={"gte": int(workload_min)}))

            if workload_max := request.query_params.get("workload_max"):
                filters.append(Q("range", workload={"lte": int(workload_max)}))

            if start_date_from := request.query_params.get("start_date_from"):
                filters.append(Q("range", start_date={"gte": start_date_from}))

            if start_date_to := request.query_params.get("start_date_to"):
                filters.append(Q("range", start_date={"lte": start_date_to}))

            s = s.query(Q("bool", must=filters))

            if ordering:
                if ordering.startswith("-"):
                    s = s.sort({ordering[1:]: {"order": "desc"}})
                else:
                    s = s.sort(ordering)

            pages = self.paginate_queryset(s)
            if pages:
                data = [hit.to_dict() for hit in pages]
                serializer = CourseSearchSerializer(data, many=True)
                return self.get_paginated_response(serializer.data)

            results = [hit.to_dict() for hit in s.execute()]
            serializer = CourseSearchSerializer(results, many=True)
            return self.get_paginated_response(serializer.data)

        else:

            try:

                if not ordering:
                    ordering = '-created_at'

                queryset = Course.objects.annotate(
                    avg_rating=Avg("ratings__rating"),
                    paid_count=Count("payments", filter=Qdjango(payments__status="paid"))  # noqa: E501
                )

                page = self.paginate_queryset(queryset)
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            except Exception as e:
                return Response(
                    {'detail': str(e)},
                    status=status.HTTP_400_BAD_REQUEST
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

        notification_users_course(notification.id)
