from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from .models import Team, Project, Task, TaskComment
from .serializers import (
    TeamSerializer,
    ProjectSerializer,
    TaskSerializer,
    UserSerializer,
    TaskCommentSerializer
)
from django.contrib.auth.models import User


class TeamViewSet(ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TaskCommentViewSet(ModelViewSet):
    """
    ViewSet obsługujący komentarze przypisane do konkretnego zadania.
    """
    serializer_class = TaskCommentSerializer
    permission_classes = [IsAuthenticated]  # Komentarze tylko dla zalogowanych użytkowników.

    def get_queryset(self):
        """
        Zwraca tylko komentarze powiązane z zadaniem o określonym `task_id`.
        """
        task_id = self.kwargs.get('task_id')  # Pobranie ID zadania z URL-a
        if not task_id:
            raise NotFound("Nie podano ID zadania.")
        return TaskComment.objects.filter(task__id=task_id)

    def perform_create(self, serializer):
        """
        Tworzy komentarz powiązany z zadaniem o określonym `task_id`.
        """
        task_id = self.kwargs.get('task_id')  # Pobranie ID zadania z URL-a
        try:
            task = Task.objects.get(id=task_id)  # Znalezienie zadania
        except Task.DoesNotExist:
            raise NotFound("Zadanie o podanym ID nie istnieje.")

        # Ustawianie zadania i autora
        serializer.save(task=task, author=self.request.user)
