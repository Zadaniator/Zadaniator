from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework.serializers import ModelSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# Serializer do obsługi User
class RegisterUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']  # Pola, które muszą być podane w body
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Tworzenie nowego użytkownika z zapisanym hasłem w postaci hash
        user = User.objects.create_user(**validated_data)
        return user


# Widok endpointu rejestracji
class RegisterUserView(APIView):
    permission_classes = [AllowAny]  # Brak wymogu autentykacji
    serializer_class = RegisterUserSerializer  # Określamy serializer dla widoku

    # Dekorator do generowania dokumentacji Swaggera
    @swagger_auto_schema(
        request_body=RegisterUserSerializer,  # Dokumentacja body requestu na podstawie serializera
        responses={
            201: openapi.Response('User created successfully'),
            400: openapi.Response('Validation error'),  # W przypadku błędów walidacji
        }
    )
    def post(self, request, *args, **kwargs):
        # Obsługa żądania POST
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
