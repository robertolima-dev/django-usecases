import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

from .models import Message, Room

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = await self.get_user_from_token()
        if not self.user:
            await self.close()
            return

        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.room_group_name = f"private_chat_room_{self.room_id}"
        self.room = await self.get_room(self.room_id)

        if self.room and await self.is_participant(self.room, self.user): # noqa501
            await self.channel_layer.group_add(self.room_group_name, self.channel_name) # noqa501
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name) # noqa501

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get("message")

        msg = await self.create_message(self.user, self.room, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": msg.content,
                "sender_id": msg.sender.id,
                "sender_username": msg.sender.username,
                "timestamp": str(msg.timestamp)
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "sender_id": event["sender_id"],
            "sender_username": event["sender_username"],
            "timestamp": event["timestamp"]
        }))

    # ============================
    # Métodos auxiliares
    # ============================

    @database_sync_to_async
    def get_user_from_token(self):
        try:
            query_string = self.scope["query_string"].decode()
            token_key = query_string.split("token=")[-1]
            token = Token.objects.get(key=token_key)
            return token.user
        except Exception:
            return None

    @database_sync_to_async
    def get_room(self, room_id):
        try:
            return Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            return None

    @database_sync_to_async
    def is_participant(self, room, user):
        return user == room.user1 or user == room.user2

    @database_sync_to_async
    def create_message(self, sender, room, content):
        return Message.objects.create(sender=sender, room=room, content=content) # noqa501
