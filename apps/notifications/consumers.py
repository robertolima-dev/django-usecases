import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser
from rest_framework.authtoken.models import Token

from apps.notifications.models import Notification


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        token_key = self.scope["query_string"].decode().split("token=")[-1]
        self.user = await self.get_user_from_token(token_key)

        if self.user is None or isinstance(self.user, AnonymousUser):
            await self.close()
        else:
            self.group_name = f"user_{self.user.id}"
            await self.channel_layer.group_add(self.group_name, self.channel_name)  # noqa: E501
            await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)  # noqa: E501

    async def receive(self, text_data):
        data = json.loads(text_data)
        title = data.get("title")
        message = data.get("message")

        notification = await self.create_notification(title, message)

        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "send_notification",
                "title": notification.title,
                "message": notification.message,
                "created_at": str(notification.created_at),
            }
        )

    async def send_notification(self, event):
        await self.send(text_data=json.dumps({
            "title": event["title"],
            "message": event["message"],
            "created_at": event["created_at"],
        }))

    @database_sync_to_async
    def get_user_from_token(self, token):
        try:
            return Token.objects.get(key=token).user
        except Token.DoesNotExist:
            return None

    @database_sync_to_async
    def create_notification(self, title, message):
        return Notification.objects.create(
            user=self.user,
            title=title,
            message=message
        )
