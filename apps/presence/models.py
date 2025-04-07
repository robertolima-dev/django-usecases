from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class UserPresence(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="online_status") # noqa501
    is_online = models.BooleanField(default=False)
    last_seen = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} - {'Online' if self.is_online else 'Offline'}"
