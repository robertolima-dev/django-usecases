import json
import logging

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework.authtoken.models import Token

from .models import Message, Room

logger = logging.getLogger(__name__)

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # print(f"[WEBSOCKET] Conexão recebida para sala: {self.scope['url_route']['kwargs']['room_name']}") # noqa501
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        token_key = self.scope["query_string"].decode().split("token=")[-1]
        self.user = await self.get_user_from_token(token_key)

        if self.user is None or isinstance(self.user, AnonymousUser):
            await self.close()
        else:
            await self.channel_layer.group_add(self.room_group_name, self.channel_name) # noqa501
            await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name) # noqa501

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["message"]

        await self.save_message(self.user, self.room_name, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "user": self.user.username,
                "message": message,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "user": event["user"],
            "message": event["message"]
        }))

    @database_sync_to_async
    def get_user_from_token(self, token):
        # logger.info(f"Token recebido no socket: {token}")
        try:
            return Token.objects.get(key=token).user
        except Token.DoesNotExist:
            return None

    @database_sync_to_async
    def save_message(self, user, room_name, message):
        room, _ = Room.objects.get_or_create(name=room_name)
        return Message.objects.create(user=user, room=room, content=message)
