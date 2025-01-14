from rest_framework.viewsets import ModelViewSet
from .models import Team, Project, Task
from .serializers import TeamSerializer, ProjectSerializer, TaskSerializer, UserSerializer
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
