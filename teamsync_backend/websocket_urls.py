from django.urls import re_path
from .consumers import TeamChatConsumer  # Import Konsumera

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<team_name>\w+)/$', TeamChatConsumer.as_asgi()),
]