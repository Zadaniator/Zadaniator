from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..models import ChatMessage


class ChatHistoryView(APIView):
    permission_classes = [IsAuthenticated]  # Wymagana autoryzacja użytkownika

    def get(self, request, room_name):
        # Pobierz wiadomości z podanego pokoju, posortowane według czasu ich dodania
        messages = ChatMessage.objects.filter(room=room_name).order_by('timestamp')

        # Sformatuj dane w czytelnej formie JSON
        return Response([
            {
                "username": message.user.username,
                "message": message.message,
                "timestamp": message.timestamp
            }
            for message in messages
        ])
