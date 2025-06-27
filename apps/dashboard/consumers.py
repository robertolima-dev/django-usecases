import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework.authtoken.models import Token

from apps.book.models import Book
from apps.course.models import Course
from apps.report.models import ReportRequest

User = get_user_model()


class DashboardConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        token_key = self.scope["query_string"].decode().split("token=")[-1]
        self.user = await self.get_user_from_token(token_key)

        if self.user is None or isinstance(self.user, AnonymousUser):
            await self.close()
        else:
            self.group_name = "dashboard"
            await self.channel_layer.group_add(self.group_name, self.channel_name)  # noqa: E501
            await self.accept()
            await self.send_dashboard_data()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)  # noqa: E501

    async def receive(self, text_data):
        # Poderia implementar filtros ou atualizações futuras
        pass

    async def send_dashboard_data(self):
        data = await self.get_dashboard_data()
        await self.send(text_data=json.dumps(
            {
                "type": "start_dashboard",
                "data": {
                    "type": "dashboard_data",
                    **data
                }
            })
        )

    async def dashboard_update(self, event):
        await self.send_dashboard_data()

    async def send_admin_event(self, event):
        await self.send(text_data=json.dumps({
            "event_type": event["event_type"],
            "data": event["data"]
        }))

    async def send_dashboard_update(self, event):
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def get_user_from_token(self, token):
        try:
            return Token.objects.get(key=token).user
        except Token.DoesNotExist:
            return None

    @database_sync_to_async
    def get_dashboard_data(self):
        return {
            "users_count": User.objects.count(),
            "courses_count": Course.objects.count(),
            "reports_count": ReportRequest.objects.count(),
            "books_count": Book.objects.count(),
        }
