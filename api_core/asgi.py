"""
ASGI config for api_core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

# import os

# from django.core.asgi import get_asgi_application

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api_core.settings")

# application = get_asgi_application()

import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api_core.settings")
django.setup()

from channels.auth import AuthMiddlewareStack  # noqa
from channels.routing import ProtocolTypeRouter, URLRouter  # noqa
from django.core.asgi import get_asgi_application  # noqa

import apps.chat.routing  # noqa
import apps.dashboard.routing  # noqa
import apps.notifications.routing  # noqa
import apps.presence.routing  # noqa

print("[ASGI] Aplicação ASGI iniciada")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            apps.chat.routing.websocket_urlpatterns +
            apps.notifications.routing.websocket_urlpatterns +
            apps.presence.routing.websocket_urlpatterns +
            apps.dashboard.routing.websocket_urlpatterns
        )
    ),
})
