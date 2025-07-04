# reports/views.py
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from apps.report.models import ReportRequest
from apps.report.tasks import generate_user_report

from .serializers import ReportRequestSerializer


@extend_schema(
    tags=["Reports"]
)
class ReportRequestViewSet(ModelViewSet):
    queryset = ReportRequest.objects.select_related("user").order_by("-created_at")  # noqa: E501
    serializer_class = ReportRequestSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        report = serializer.save(user=self.request.user, status="pending")
        generate_user_report.delay(report.id)
