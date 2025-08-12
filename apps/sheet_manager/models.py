from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from api_core.models import BaseModel

# Create your models here.
TYPE_OF_DATA_CHOICES = (
    ('financial_data', 'financial_data'),
    # ('', ''),
    # ('', ''),
    # ('', ''),
    # ('', ''),
    # ('', ''),
)

TYPE_SHEET_DATA_CHOICES = (
    ('header', 'Header'),
    ('body', 'Body'),
)


class SafeFileField(models.FileField):
    """Campo de arquivo que lida melhor com erros de storage"""
    
    def save_form_data(self, instance, data):
        """Salva o arquivo de forma segura"""
        if data is not None:
            try:
                # Tentar salvar normalmente
                super().save_form_data(instance, data)
            except Exception as e:
                if "Required parameter name not set" in str(e):
                    # Se for erro do S3, salvar manualmente
                    try:
                        file_content = data.read()
                        data.seek(0)  # Resetar cursor
                        
                        # Salvar usando storage diretamente
                        file_path = default_storage.save(
                            f"sheet_uploads/{data.name}", 
                            ContentFile(file_content)
                        )
                        
                        # Definir o caminho do arquivo
                        setattr(instance, self.name, file_path)
                    except Exception as manual_error:
                        raise ValidationError(f"Erro ao salvar arquivo: {manual_error}")
                else:
                    raise e


class ManagerSheet(BaseModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, db_index=True)  # noqa: E501
    file = SafeFileField(upload_to="sheet_uploads/")
    formatter = models.JSONField(null=True, blank=True)
    table_html = models.TextField(null=True, blank=True)
    type_of_data = models.CharField(
        choices=TYPE_OF_DATA_CHOICES,
        max_length=120,
        null=True,
    )

    def __str__(self):
        user_info = self.user.email if self.user else "No user"
        return f"ManagerSheet {self.id} - User {user_info}"

    def clean(self):
        """Validação customizada"""
        if not self.file:
            raise ValidationError("O arquivo é obrigatório.")
        
        # Verifica se o arquivo tem um nome válido
        if self.file and not self.file.name:
            raise ValidationError("O arquivo deve ter um nome válido.")

    def get_file_url(self):
        """Retorna a URL do arquivo de forma segura"""
        try:
            if self.file and self.file.name:
                return self.file.url
            return None
        except Exception:
            return None

    def get_file_name(self):
        """Retorna o nome do arquivo de forma segura"""
        try:
            if self.file and self.file.name:
                return self.file.name.split('/')[-1]
            return "Arquivo não encontrado"
        except Exception:
            return "Arquivo não encontrado"

    def file_exists(self):
        """Verifica se o arquivo existe no storage"""
        try:
            if self.file and self.file.name:
                return self.file.storage.exists(self.file.name)
            return False
        except Exception:
            return False


class SheetPureData(BaseModel):
    manager_sheet = models.ForeignKey(ManagerSheet, on_delete=models.CASCADE, related_name="pure_data", db_index=True)  # noqa: E501
    type_data = models.CharField(
        max_length=10,
        choices=TYPE_SHEET_DATA_CHOICES,
        default='body'
    )
    sheet_line = models.JSONField(null=True, blank=True)
    sanitized = models.BooleanField(default=False)

    def __str__(self):
        return f"PureData {self.id} - {self.type_data}"


class SheetSanitizedData(BaseModel):
    manager_sheet = models.ForeignKey(ManagerSheet, on_delete=models.CASCADE, related_name="sanitized_data", db_index=True)  # noqa: E501
    type_data = models.CharField(
        max_length=10,
        choices=TYPE_SHEET_DATA_CHOICES,
        default='body'
    )
    sheet_line = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"SanitizedData {self.id} - {self.type_data}"
