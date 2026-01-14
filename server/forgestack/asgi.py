import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack
import users.routing
import chat.routing
import courses.routing
import progress.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "forgestack.settings")

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        # HTTP requests go to Django’s ASGI handler
        "http": django_asgi_app,
        # WebSocket requests go through middleware → your routing
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(
                URLRouter(
                    users.routing.websocket_urlpatterns
                    + chat.routing.websocket_urlpatterns
                    + courses.routing.websocket_urlpatterns
                    + progress.routing.websocket_urlpatterns
                )
            )
        ),
    }
)
