from projects.models import Project
from django.db import models

# Create your models here.


class Vault(models.Model):
    project = models.OneToOneField(
        Project, on_delete=models.CASCADE, related_name="vault"
    )

    def __str__(self) -> str:
        return f"Vault for {self.project.title}"


class Secret(models.Model):
    vault = models.ForeignKey(Vault, on_delete=models.CASCADE, related_name="secrets")
    name = models.CharField(max_length=100)
    value = models.TextField()

    def __str__(self) -> str:
        return f"{self.name} in {self.vault.project.title}"
