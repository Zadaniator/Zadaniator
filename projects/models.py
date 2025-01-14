from django.db import models
from django.contrib.auth.models import User


# Model Zespołu (Team)
class Team(models.Model):
    name = models.CharField(max_length=255)  # Nazwa zespołu
    members = models.ManyToManyField(User, related_name="teams")  # Użytkownicy przypisani do zespołu

    def __str__(self):
        return self.name


# Model Projektu (Project)
class Project(models.Model):
    name = models.CharField(max_length=255, unique=True)  # Nazwa projektu (unikatowa)
    description = models.TextField(blank=True, null=True)  # Opcjonalny opis projektu
    created_at = models.DateTimeField(auto_now_add=True)  # Data utworzenia projektu
    updated_at = models.DateTimeField(auto_now=True)  # Data ostatniej aktualizacji
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="projects")  # Przypisanie zespołu do projektu

    def __str__(self):
        return self.name


# Model Zadania (Task)
class Task(models.Model):
    title = models.CharField(max_length=255)  # Tytuł zadania
    description = models.TextField(blank=True, null=True)  # Opcjonalny opis zadania
    completed = models.BooleanField(default=False)  # Status zadania: ukończone/niewykonane
    project = models.ForeignKey(Project, on_delete=models.CASCADE,
                                related_name="tasks")  # Projekt, do którego należy zadanie
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name="tasks")  # Użytkownik przypisany do zadania

    def __str__(self):
        return self.title
