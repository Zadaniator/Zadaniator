from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Team, Project, Task, TaskComment
from .serializers import TeamSerializer, ProjectSerializer, TaskSerializer, UserSerializer, TaskCommentSerializer
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
    serializer_class = TaskCommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        task_id = self.kwargs.get('task_id')
        if not task_id:
            raise NotFound("Nie podano ID zadania.")
        return TaskComment.objects.filter(task__id=task_id)

    def perform_create(self, serializer):
        task_id = self.kwargs.get('task_id')
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            raise NotFound("Zadanie o podanym ID nie istnieje.")
        serializer.save(task=task, author=self.request.user)


class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        teams = user.teams.all()
        projects = set()
        for team in teams:
            projects.update(team.projects.all())

        data = {
            "user": UserSerializer(user).data,
            "teams": TeamSerializer(teams, many=True).data,
            "projects": ProjectSerializer(projects, many=True).data
        }

        return Response(data)
