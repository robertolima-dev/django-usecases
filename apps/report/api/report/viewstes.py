# reports/views.py
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from apps.report.models import ReportRequest
from apps.report.tasks import generate_user_report

from .serializers import ReportRequestSerializer


class ReportRequestViewSet(ModelViewSet):
    queryset = ReportRequest.objects.select_related("user").order_by("-created_at") # noqa501
    serializer_class = ReportRequestSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        report = serializer.save(user=self.request.user, status="pending")
        print(report)
        generate_user_report.delay(report.id)
