"""
ASGI config for server project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application


# Set this first to avoid any ORM issues with `AuthMiddlewareStack`.
default_asgi_application = get_asgi_application()


from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from channels.sessions import SessionMiddlewareStack

from socket_config import routing


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')

application = ProtocolTypeRouter({
    'http': default_asgi_application,
    'websocket': 
        AllowedHostsOriginValidator(
        SessionMiddlewareStack(
            URLRouter(
                 routing.websocket_urlpatterns
            )
        )
    ),
})
