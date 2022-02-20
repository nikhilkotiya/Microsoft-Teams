import os
import django
from channels.routing import ProtocolTypeRouter , URLRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Microsoft_Teams.settings')
django.setup()

from channels.auth import AuthMiddleware, AuthMiddlewareStack
from chat.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket":AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    )
})