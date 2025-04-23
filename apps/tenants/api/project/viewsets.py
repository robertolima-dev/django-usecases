from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from apps.tenants.mixins import TenantQuerysetMixin
from apps.tenants.models import Project

from .serializers import ProjectSerializer


@extend_schema(
    tags=["Tenants"]
)
class ProjectViewSet(TenantQuerysetMixin, ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
