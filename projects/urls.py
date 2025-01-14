from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import TeamViewSet, ProjectViewSet, TaskViewSet, UserViewSet
from .features.user_register import RegisterUserView
from .features.chat_get import ChatHistoryView

# Router dla endpointów API
router = DefaultRouter()
router.register(r'teams', TeamViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'tasks', TaskViewSet)
router.register(r'users', UserViewSet)

# Konfiguracja Swaggera i Redoc
schema_view = get_schema_view(
    openapi.Info(
        title="Moje API",
        default_version='v1',
        description="Dokumentacja API dla mojego projektu",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="kontakt@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,  # Publiczny dostęp do dokumentacji
    permission_classes=(AllowAny,),  # Bez potrzeby uwierzytelniania
)

# Konfiguracja ścieżek (URL Patterns)
urlpatterns = [
    path('', include(router.urls)),  # Endpointy API
    path('chat/history/<str:room_name>/', ChatHistoryView.as_view(), name='chat-history'),
    path('register/', RegisterUserView.as_view(), name='register_user'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Token JWT
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Odświeżenie tokenu
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),  # Swagger UI
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),  # Redoc
]
