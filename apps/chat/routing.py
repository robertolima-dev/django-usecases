from django.urls import re_path

from apps.chat import consumers

print("[ROUTING] websocket_urlpatterns carregado")

websocket_urlpatterns = [
    re_path(r"ws/chat/room/(?P<room_id>\d+)/$", consumers.ChatConsumer.as_asgi()),  # noqa: E501
]
