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
    progress = models.PositiveIntegerField(default=0)  # Procent ukończenia zadania (0-100%)
    story_points = models.PositiveIntegerField(null=True, blank=True)  # Story points zadania do oszacowania trudności
    completed = models.BooleanField(default=False)  # Status zadania: ukończone/niewykonane
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="created_tasks"
    )  # Osoba tworząca zadanie
    assigned_to = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="working_tasks"
    )  # Użytkownik przypisany do zadania (w trakcie pracy)
    tester = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="testing_tasks"
    )  # Tester odpowiadający za testowanie zadania
    project = models.ForeignKey(Project, on_delete=models.CASCADE,
                                related_name="tasks")  # Projekt, do którego należy zadanie
    created_at = models.DateTimeField(auto_now_add=True)  # Data utworzenia zadania
    updated_at = models.DateTimeField(auto_now=True)  # Data ostatniej aktualizacji zadania

    def __str__(self):
        return self.title

class ChatMessage(models.Model):
    room = models.CharField(max_length=255)  # Nazwa pokoju czatu
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Użytkownik
    message = models.TextField()  # Treść wiadomości
    timestamp = models.DateTimeField(auto_now_add=True)  # Czas wysłania wiadomości

    def __str__(self):
        return f"{self.user.username} in {self.room}: {self.message[:20]}"


# Model Komentarzy do Zadań (TaskComment)
class TaskComment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE,
                             related_name="comments")  # Zadanie, do którego komentarz się odnosi
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")  # Autor komentarza
    content = models.TextField()  # Treść komentarza
    created_at = models.DateTimeField(auto_now_add=True)  # Data dodania komentarza
    updated_at = models.DateTimeField(auto_now=True)  # Data ostatniej aktualizacji komentarza

    def __str__(self):
        return f"Comment by {self.author.username} on {self.task.title}"
