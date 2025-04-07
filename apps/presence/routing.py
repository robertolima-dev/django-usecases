from django.urls import re_path

from .consumers import PresenceConsumer

websocket_urlpatterns = [
    re_path(r"ws/presence/$", PresenceConsumer.as_asgi()),
]
