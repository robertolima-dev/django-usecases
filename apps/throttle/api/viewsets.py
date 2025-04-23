from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.report.api.report.serializers import ReportRequestSerializer
from apps.throttle.utils import check_and_increment_quota
from common.decorators.quota import check_quota


@extend_schema(
    tags=["Throttles"]
)
class UploadViewSet(ModelViewSet):
    serializer_class = ReportRequestSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']

    @check_quota(action="upload")
    def create(self, request, *args, **kwargs):

        try:

            check_and_increment_quota(request.user, "upload")
            return Response(
                {"message": "Upload feito com sucesso!"},
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
