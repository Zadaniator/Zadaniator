import json
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatMessage
from django.contrib.auth.models import User


class TeamChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Odczytaj nazwę pokoju z adresu URL
        self.team_name = self.scope['url_route']['kwargs']['team_name']
        self.room_group_name = f"team_{self.team_name}"

        # Dołącz klienta do grupy czatu
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Usuń klienta z grupy czatu
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Przetwarzanie przychodzących danych z klienta WebSocket
        data = json.loads(text_data)
        username = data['username']
        message = data['message']

        # Zapisanie wiadomości do bazy danych
        await self.save_message(self.team_name, username, message)

        # Rozesłanie wiadomości do grupy czatu
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username
            }
        )

    async def chat_message(self, event):
        # Metoda do wysyłania wiadomości z grupy WebSocket
        message = event['message']
        username = event['username']

        # Wyślij dane do klienta WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))

    @sync_to_async
    def save_message(self, room, username, message):
        # Zapisz wiadomość w PostgreSQL
        try:
            user = User.objects.get(username=username)
            ChatMessage.objects.create(room=room, user=user, message=message)
        except User.DoesNotExist:
            pass  # Jeśli użytkownika nie ma w bazie (opcjonalna obsługa błędu)
