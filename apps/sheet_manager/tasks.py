import csv
from io import TextIOWrapper

from celery import shared_task
from django.core.files.storage import default_storage

from .models import ManagerSheet, SheetPureData


@shared_task
def process_uploaded_sheet(manager_sheet_id):
    try:
        manager_sheet = ManagerSheet.objects.get(id=manager_sheet_id)
        file_path = manager_sheet.file.name

        with default_storage.open(file_path, 'rb') as f:
            reader = csv.reader(TextIOWrapper(f, encoding='utf-8'))

            is_header = True
            for line in reader:
                SheetPureData.objects.create(
                    manager_sheet=manager_sheet,
                    type_data='header' if is_header else 'body',
                    sheet_line=line,
                    sanitized=False
                )
                is_header = False

        # (Opcional) Chamar próxima task de saneamento aqui depois

    except Exception as e:
        # Log de erro para observabilidade
        print(f"Erro ao processar planilha ID {manager_sheet_id}: {e}")
