from django.db import models


class EmailTemplate(models.Model):
    name = models.CharField(max_length=100, unique=True)
    subject = models.CharField(max_length=200)
    html_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class EmailLog(models.Model):
    recipient = models.EmailField()
    subject = models.CharField(max_length=200)
    template = models.ForeignKey(EmailTemplate, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, default='pending')
    response = models.TextField(blank=True, null=True)
    context = models.JSONField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.recipient} - {self.subject}"
