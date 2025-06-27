from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Room(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)  # noqa: E501
    users = models.ManyToManyField(User, related_name='rooms')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_rooms')  # noqa: E501
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_private(self):
        return self.users.count() == 2

    def __str__(self):
        return self.name or f"Private chat ({', '.join(u.username for u in self.users.all())})"  # noqa: E501


class Message(models.Model):
    TYPE_CHOICES = [
        ('text', 'Texto'),
        ('image', 'Imagem'),
        ('link', 'Link'),
        ('file', 'Arquivo'),
        ('system', 'Sistema'),
    ]

    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)  # noqa: E501
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    type_message = models.CharField(max_length=10, choices=TYPE_CHOICES, default='text')  # noqa: E501
    content = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
