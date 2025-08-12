import traceback

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from rest_framework import permissions, status, viewsets
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.sheet_manager.models import ManagerSheet
from apps.sheet_manager.tasks import process_uploaded_sheet

from .serializers import ManagerSheetSerializer


class SheetUploadAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        try:
            print("=== DEBUG UPLOAD ===")
            print(f"FILES: {request.FILES}")
            print(f"DATA: {request.data}")

            # Verificar se há arquivo
            if 'file' not in request.FILES:
                return Response(
                    {"error": "Nenhum arquivo enviado."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            file_obj = request.FILES['file']
            print(f"File object: {file_obj}")
            print(f"File name: {file_obj.name}")
            print(f"File size: {file_obj.size}")

            # Validar o arquivo
            if not file_obj.name:
                return Response(
                    {"error": "Arquivo deve ter um nome válido."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Verificar extensão
            allowed_extensions = ['.xlsx', '.xls', '.csv']
            file_extension = file_obj.name.lower()
            if not any(file_extension.endswith(ext) for ext in allowed_extensions):  # noqa: E501
                return Response(
                    {"error": f"Formato de arquivo não suportado. Use: {', '.join(allowed_extensions)}"},  # noqa: E501
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Abordagem direta: salvar o arquivo primeiro, depois criar o objeto  # noqa: E501
            try:
                # Ler o conteúdo do arquivo
                file_content = file_obj.read()
                file_obj.seek(0)  # Resetar o cursor

                # Salvar o arquivo usando o storage
                file_path = default_storage.save(
                    f"sheet_uploads/{file_obj.name}",
                    ContentFile(file_content)
                )

                print(f"Arquivo salvo: {file_path}")

                # Criar o ManagerSheet com o caminho do arquivo
                manager_sheet = ManagerSheet.objects.create(
                    user=request.user,
                    file=file_path,
                    type_of_data=request.data.get('type_of_data')
                )

                print(f"ManagerSheet criado: {manager_sheet}")

            except Exception as save_error:
                print(f"Erro ao salvar arquivo: {save_error}")
                print(f"Traceback: {traceback.format_exc()}")
                return Response(
                    {"error": f"Erro ao salvar arquivo: {str(save_error)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            # Disparar Task Celery (descomente se necessário)
            process_uploaded_sheet.delay(manager_sheet_id=manager_sheet.id)

            # Retornar dados usando o serializer
            response_serializer = ManagerSheetSerializer(manager_sheet)

            return Response({
                "message": "Upload recebido. Em processamento.",
                "data": response_serializer.data
            }, status=status.HTTP_202_ACCEPTED)

        except Exception as e:
            print(f"Erro no upload: {str(e)}")
            print(f"Traceback completo: {traceback.format_exc()}")
            return Response(
                {'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class ManagerSheetViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar ManagerSheets
    """
    serializer_class = ManagerSheetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Retorna apenas os ManagerSheets do usuário logado"""
        return ManagerSheet.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Define o usuário automaticamente ao criar"""
        serializer.save(user=self.request.user)

    def list(self, request, *args, **kwargs):
        """Lista os ManagerSheets com informações de status dos arquivos"""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        # Adicionar estatísticas
        total = queryset.count()
        files_exist = sum(1 for ms in queryset if ms.file_exists())
        files_missing = total - files_exist

        return Response({
            'data': serializer.data,
            'stats': {
                'total': total,
                'files_exist': files_exist,
                'files_missing': files_missing
            }
        })
