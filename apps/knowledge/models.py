from django.contrib.auth import get_user_model
from django.db import models


class KnowledgeTopic(models.Model):
    LEVELS = [
        ("fundamental", "Fundamental"),
        ("intermediate", "Intermediário"),
        ("advanced", "Avançado"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    level = models.CharField(max_length=20, choices=LEVELS)
    is_recommended = models.BooleanField(default=True)

    class Meta:
        ordering = ["level", "title"]

    def __str__(self):
        return self.title


User = get_user_model()


class KnowledgeStudy(models.Model):
    topic = models.ForeignKey("KnowledgeTopic", on_delete=models.CASCADE, related_name="studies") # noqa501
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    studied_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-studied_at"]
        unique_together = ("topic", "user")  # um estudo por usuário por tópico

    def __str__(self):
        return f"{self.user} estudou {self.topic}"
