from rest_framework import permissions, status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.sheet_manager.models import ManagerSheet
from apps.sheet_manager.tasks import process_uploaded_sheet


class SheetUploadAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({"error": "Arquivo não enviado."}, status=status.HTTP_400_BAD_REQUEST)  # noqa: E501

        manager_sheet = ManagerSheet.objects.create(
            user=request.user,
            file=file
        )

        # Disparar Task Celery
        process_uploaded_sheet.delay(manager_sheet.id)

        return Response({
            "message": "Upload recebido. Em processamento.",
            "manager_sheet_id": manager_sheet.id
        }, status=status.HTTP_202_ACCEPTED)
