from django.urls import re_path

from apps.notifications import consumers

print("[ROUTING] websocket_urlpatterns carregado")

websocket_urlpatterns = [
    re_path(r"ws/notifications/$", consumers.NotificationConsumer.as_asgi()),
]
