from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenRefreshView
from .views import TeamViewSet, ProjectViewSet, TaskViewSet, UserViewSet, TaskCommentViewSet, UserDetailView
from .features.user_register import RegisterUserView
from .features.chat_get import ChatHistoryView
from .features.custom_jwt import CustomTokenObtainPairView


router = DefaultRouter()
router.register(r'teams', TeamViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'tasks', TaskViewSet)
router.register(r'users', UserViewSet)


schema_view = get_schema_view(
    openapi.Info(
        title="Moje API",
        default_version='v1',
        description="Dokumentacja API dla mojego projektu",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="kontakt@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(AllowAny,),
)

urlpatterns = [
    path('', include(router.urls)),
    path('tasks/<int:task_id>/comments/', TaskCommentViewSet.as_view({'get': 'list', 'post': 'create'}),
         name='task-comments'),
    path('tasks/<int:task_id>/comments/<int:pk>/', TaskCommentViewSet.as_view(
        {'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}),
         name='task-comment-detail'),
    path('chat/history/<str:room_name>/', ChatHistoryView.as_view(), name='chat-history'),
    path('register/', RegisterUserView.as_view(), name='register_user'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('me/', UserDetailView.as_view(), name='user_detail'),
]
