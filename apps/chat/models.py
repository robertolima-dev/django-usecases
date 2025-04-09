from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Room(models.Model):
    user1 = models.ForeignKey(User, related_name='chat_user1', on_delete=models.CASCADE, null=True, blank=True) # noqa501
    user2 = models.ForeignKey(User, related_name='chat_user2', on_delete=models.CASCADE, null=True, blank=True) # noqa501
    created_at = models.DateTimeField(auto_now_add=True)

    # class Meta:
    #     unique_together = ('user1', 'user2')

    def __str__(self):
        return f"Chat: {self.user1.username} <-> {self.user2.username}"

    def get_room_name(self):
        return f"room_{min(self.user1.id, self.user2.id)}_{max(self.user1.id, self.user2.id)}" # noqa501


class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE) # noqa501
    sender = models.ForeignKey(
        User,
        related_name='sent_messages',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']
