"""
ASGI config for mysite project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os
# import django #maybe delete

from django.core.asgi import get_asgi_application

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
import studybuddy.routing

from django.urls import re_path

from studybuddy import consumers

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
# django.setup() #maybe delete

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    # "websocket": AuthMiddlewareStack(
    #     URLRouter(
    #         studybuddy.routing.websocket_urlpatterns
    #     )
    # )

    "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(
                URLRouter(
                    studybuddy.routing.websocket_urlpatterns
                    # [re_path(r'ws/studybuddy/chat/rooms/(?P<room_name>\w+)$/', consumers.ChatConsumer.as_asgi())]
                )
            )
        )
})