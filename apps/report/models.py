# reports/models.py
from django.contrib.auth.models import User
from django.db import models

STATUS_CHOICES = (
    ("pending", "Pendente"),
    ("processing", "Processando"),
    ("done", "Concluído"),
    ("failed", "Falhou"),
)


class ReportRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")  # noqa: E501
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    file_path = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Relatório de {self.user.username} - {self.status}"
