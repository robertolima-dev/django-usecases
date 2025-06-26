from django.db import models

REQUEST_TYPES_CHOICES = (
    ('success', 'success'),
    ('error', 'error'),
)


# Create your models here.
class HttpCallLog(models.Model):
    url = models.URLField()
    method = models.CharField(max_length=10)
    status_code = models.IntegerField(null=True, blank=True)
    response_time = models.FloatField(null=True, blank=True, help_text="Tempo em segundos")  # noqa: E501
    response_body = models.TextField(null=True, blank=True)
    error_message = models.TextField(null=True, blank=True)
    request_type = models.CharField(
        choices=REQUEST_TYPES_CHOICES,
        max_length=20,
        default='error'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.method.upper()} {self.url} [{self.status_code}]"
