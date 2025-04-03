# reports/serializers.py
from rest_framework import serializers

from apps.report.models import ReportRequest


class ReportRequestSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ReportRequest
        fields = [
            "id",
            "user",
            "status",
            "created_at",
            "completed_at",
            "file_path"
        ]
        read_only_fields = [
            "user",
            "status",
            "created_at",
            "completed_at",
            "file_path"
        ]
