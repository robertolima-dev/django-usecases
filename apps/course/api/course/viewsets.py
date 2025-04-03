# course/views.py
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.viewsets import ModelViewSet

from apps.course.filters import CourseFilter
from apps.course.models import Course

from .serializers import CourseSerializer


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.select_related("category", "instructor__user").prefetch_related("tags") # noqa501
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = CourseFilter
    search_fields = ["title", "description"]
    ordering_fields = ["price", "workload", "start_date", "created_at"]
    ordering = ["-created_at"]
