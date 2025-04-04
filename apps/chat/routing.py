from django.urls import re_path

from apps.chat import consumers

print("[ROUTING] websocket_urlpatterns carregado")

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
]
