import os
import time
from io import BytesIO

from django.core.files.base import ContentFile
from django.utils.text import slugify
from drf_spectacular.utils import extend_schema
from PIL import Image
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.image_processing.models import UploadedImage
from apps.image_processing.permissions import IsSqsAuthenticated

from .serializers import UploadedImageSerializer


@extend_schema(
    tags=["Image processing"]
)
class ImageUploadAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):

        try:

            serializer = UploadedImageSerializer(data=request.data, context={'request': request}) # noqa501
            if serializer.is_valid():

                serializer.save()

                return Response({
                    "message": "Imagem enviada com sucesso!",
                    "id": request.user.image.last().id,
                    "image": request.user.image.last().original_image.url,
                    "thumbnail": None,
                    "thumbnail-status": "processing",
                })

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) # noqa501

        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST) # noqa501


@extend_schema(
    tags=["Image processing"]
)
class UserImageListAPIView(ListAPIView):
    serializer_class = UploadedImageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UploadedImage.objects.filter(user=self.request.user).order_by("-uploaded_at") # noqa501


class ImageProcessingSyncApiView(APIView):
    permission_classes = [IsSqsAuthenticated]
    authentication_classes = []

    def post(self, request):

        try:
            image_instance = UploadedImage.objects.get(id=request.data['image_id']) # noqa501
            time.sleep(1)

            original_path = image_instance.original_image.path
            image = Image.open(original_path).convert("RGB")
            base_name, _ = os.path.splitext(os.path.basename(original_path)) # noqa501
            base_slug = slugify(base_name)

            output_format = image_instance.output_format or 'JPEG'
            ext = 'webp' if output_format == 'WEBP' else 'jpg'

            sizes = {
                'thumbnail': (150, 150),
                'medium': (600, 600),
                'large': (1200, 1200),
            }

            for label, size in sizes.items():
                img_copy = image.copy()
                img_copy.thumbnail(size)

                buffer = BytesIO()
                img_copy.save(buffer, format=output_format, quality=85) # noqa501
                image_field = ContentFile(buffer.getvalue())
                filename = f"{label}_{base_slug}.{ext}"

                setattr(image_instance, label, image_field)
                getattr(image_instance, label).save(filename, image_field, save=False) # noqa501

            image_instance.save()
            return Response(
                {'detail': f"✅ Imagens geradas para {image_instance.original_image.name}"}, # noqa501
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            print(f"❌ Erro ao gerar imagens: {str(e)}")
            return Response(
                {'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
