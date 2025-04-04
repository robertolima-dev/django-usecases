from rest_framework import serializers

from apps.tenants.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'is_active', 'created_at', 'updated_at'] # noqa501
        read_only_fields = ['created_at', 'updated_at']

    def create(self, validated_data):
        tenant = self.context['request'].tenant
        return Project.objects.create(tenant=tenant, **validated_data)
