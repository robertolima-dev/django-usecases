import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework.authtoken.models import Token

from .models import UserPresence

User = get_user_model()


class PresenceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        token_key = self.scope["query_string"].decode().split("token=")[-1]
        self.user = await self.get_user_from_token(token_key)

        if not self.user or isinstance(self.user, AnonymousUser):
            await self.close()
            return

        self.group_name = "online_users"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.set_user_online()
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name) # noqa501
        await self.set_user_offline()

    async def receive(self, text_data):
        # Mensagens podem ser usadas no futuro para comandos, ex: ping
        await self.send(text_data=json.dumps({"status": "online"}))

    @database_sync_to_async
    def get_user_from_token(self, token):
        try:
            return Token.objects.get(key=token).user
        except Token.DoesNotExist:
            return None

    @database_sync_to_async
    def set_user_online(self):
        UserPresence.objects.update_or_create(
            user=self.user,
            defaults={"is_online": True}
        )

    @database_sync_to_async
    def set_user_offline(self):
        UserPresence.objects.update_or_create(
            user=self.user,
            defaults={"is_online": False}
        )
