from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Project(models.Model):
    title: str = models.CharField(max_length=50)
    description: str = models.TextField(max_length=300)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="projects")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title


class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=100)
    is_completed = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title
