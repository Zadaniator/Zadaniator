import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import myapp.routing  # Zamień `myapp` na nazwę własnej aplikacji

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'teamsync_backebd.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # HTTP obsługuje tradycyjne żądania
    "websocket": AuthMiddlewareStack(  # AuthMiddlewareStack dodaje obsługę autoryzacji użytkownika
        URLRouter(
            myapp.routing.websocket_urlpatterns  # Wskazuje na `websocket_urlpatterns`
        )
    ),
})