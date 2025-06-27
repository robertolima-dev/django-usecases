from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class UserQuota(models.Model):
    ACTION_CHOICES = (
        ("api_access", "API Access"),
        ("upload", "Upload de Arquivo"),
        ("report", "Geração de Relatório"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="quotas")  # noqa: E501
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    limit = models.PositiveIntegerField(default=100)
    used = models.PositiveIntegerField(default=0)
    reset_date = models.DateField()

    class Meta:
        unique_together = ("user", "action")

    def __str__(self):
        return f"{self.user} - {self.action}: {self.used}/{self.limit}"
