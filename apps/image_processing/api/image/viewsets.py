from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.image_processing.models import UploadedImage
from apps.image_processing.tasks import create_thumbnail

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

                create_thumbnail.delay(request.user.image.last().id)

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