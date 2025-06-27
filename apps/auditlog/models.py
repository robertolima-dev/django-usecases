from django.contrib.auth import get_user_model
from django.db import models
from django.utils.timezone import now

User = get_user_model()


class AuditLog(models.Model):
    ACTION_CHOICES = (
        ("create", "Criação"),
        ("update", "Atualização"),
        ("delete", "Exclusão"),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # noqa: E501
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    model = models.CharField(max_length=100)
    object_id = models.CharField(max_length=100)
    object_repr = models.TextField()
    changes = models.JSONField(null=True, blank=True)
    timestamp = models.DateTimeField(default=now)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"[{self.timestamp}] {self.user} - {self.action} em {self.model}({self.object_id})"  # noqa: E501
