from PIL import Image
from rest_framework import serializers

from apps.image_processing.models import UploadedImage


class UploadedImageSerializer(serializers.ModelSerializer):
    original_image = serializers.ImageField(use_url=True)
    thumbnail = serializers.ImageField(use_url=True, required=False, allow_null=True)  # noqa: E501
    medium = serializers.ImageField(use_url=True, required=False, allow_null=True)  # noqa: E501
    large = serializers.ImageField(use_url=True, required=False, allow_null=True)  # noqa: E501
    output_format = serializers.ChoiceField(choices=['JPEG', 'WEBP'], default='JPEG', write_only=True)  # noqa: E501

    class Meta:
        model = UploadedImage
        fields = [
            'id', 'original_image', 'thumbnail', 'medium', 'large',
            'uploaded_at', 'output_format'
        ]
        read_only_fields = ['id', 'user', 'thumbnail', 'medium', 'large', 'uploaded_at']  # noqa: E501

    def validate_original_image(self, image):
        max_size_mb = 5
        if image.size > max_size_mb * 1024 * 1024:
            raise serializers.ValidationError(f"Tamanho máximo permitido é {max_size_mb}MB.")  # noqa: E501

        valid_formats = ['JPEG', 'JPG', 'PNG', 'WEBP']
        img = Image.open(image)
        if img.format.upper() not in valid_formats:
            raise serializers.ValidationError(f"Formato inválido. Permitidos: {', '.join(valid_formats)}")  # noqa: E501

        min_width, min_height = 300, 300
        if img.width < min_width or img.height < min_height:
            raise serializers.ValidationError(f"A imagem deve ter no mínimo {min_width}x{min_height} pixels.")  # noqa: E501

        return image

    def create(self, validated_data):
        user = self.context['request'].user
        return UploadedImage.objects.create(user=user, **validated_data)
