from django.contrib.auth.models import User
from django.db import models

from api_core.models import BaseModel

# Create your models here.
TYPE_OF_DATA_CHOICES = (
    ('financial_data', 'financial_data'),
    # ('', ''),
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


class ManagerSheet(BaseModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, db_index=True)  # noqa: E501
    file = models.FileField(upload_to="sheet_uploads/")
    formatter = models.JSONField(null=True, blank=True)
    table_html = models.TextField(null=True, blank=True)
    type_of_data = models.CharField(
        choices=TYPE_OF_DATA_CHOICES,
        max_length=120,
        null=True,
    )

    def __str__(self):
        return f"ManagerSheet {self.id} - User {self.user_id}"


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
