from rest_framework import serializers

from apps.mediahub.models import MediaFile


class MediaFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaFile
        fields = "__all__"
        read_only_fields = ["uploaded_at"]


class MediaFileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaFile
        fields = ["id", "name", "file", "uploaded_at"]
        read_only_fields = ["id", "uploaded_at"]
