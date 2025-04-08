from rest_framework import serializers

from apps.image_processing.models import UploadedImage


class UploadedImageSerializer(serializers.ModelSerializer):
    original_image = serializers.ImageField(use_url=True)
    thumbnail = serializers.ImageField(use_url=True, required=False, allow_null=True) # noqa501

    class Meta:
        model = UploadedImage
        fields = ['id', 'original_image', 'thumbnail', 'uploaded_at']
        read_only_fields = ['id', 'user', 'thumbnail', 'uploaded_at']

    def create(self, validated_data):
        user = self.context['request'].user
        return UploadedImage.objects.create(user=user, **validated_data)
