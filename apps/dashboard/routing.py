from django.urls import re_path

from apps.dashboard import consumers

print("[ROUTING] websocket_urlpatterns carregado")

websocket_urlpatterns = [
    re_path(r"ws/dashboard/$", consumers.DashboardConsumer.as_asgi()),
]
