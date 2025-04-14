import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

from common.decorators.websocket import ensure_room_participant

from .models import Message, Room

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = await self.get_user_from_token()
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f"chat_room_{self.room_id}"

        self.room = await self.get_room(self.room_id)

        if self.user and await self.user_in_room(self.user, self.room):
            await self.channel_layer.group_add(self.room_group_name, self.channel_name) # noqa501
            await self.accept()
        else:
            await self.close()

    @ensure_room_participant(lambda scope: scope["url_route"]["kwargs"]["room_id"]) # noqa501
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name) # noqa501

    async def receive(self, text_data):
        data = json.loads(text_data)
        content = data.get("content")
        type_message = data.get("type_message", "text")  # default = text

        message = await self.create_message(self.user, self.room, type_message, content) # noqa501

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message_id": message.id,
                "sender_id": self.user.id,
                "sender_username": self.user.username,
                "content": message.content,
                "type_message": message.type_message,
                "timestamp": str(message.timestamp),
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "message_id": event["message_id"],
            "sender_id": event["sender_id"],
            "sender_username": event["sender_username"],
            "content": event["content"],
            "type_message": event["type_message"],
            "timestamp": event["timestamp"]
        }))

    # ===== Métodos auxiliares =====

    @database_sync_to_async
    def get_user_from_token(self):
        try:
            token_key = self.scope["query_string"].decode().split("token=")[-1] # noqa501
            token = Token.objects.get(key=token_key)
            return token.user
        except Token.DoesNotExist:
            return None

    @database_sync_to_async
    def get_room(self, room_id):
        try:
            return Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            return None

    @database_sync_to_async
    def user_in_room(self, user, room):
        return room.users.filter(id=user.id).exists()

    @database_sync_to_async
    def create_message(self, sender, room, type_message, content):
        return Message.objects.create(
            room=room,
            sender=sender,
            type_message=type_message,
            content=content
        )
