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

import studybuddy.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
# django.setup() #maybe delete

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            studybuddy.routing.websocket_urlpatterns
        )
    )
})