import os
from cryptography.fernet import Fernet
from projects.models import Project
from django.db import models
from django.conf import settings

# Create your models here.


FERNET_KEY = os.environ.get("ENCRYPTION_KEY")
cipher = Fernet(FERNET_KEY.encode())


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

    def save(self, *args, **kwargs):
        if self.value and not self.value.startswith("gAAAAA"):
            encrypted_value = cipher.encrypt(self.value.encode())
            self.value = encrypted_value.decode()
        super().save(*args, **kwargs)

    @property
    def decrypted_value(self):
        try:
            decrypted = cipher.decrypt(self.value.encode())
            return decrypted.decode()
        except Exception:
            return "Decipher error"

    def __str__(self) -> str:
        return f"{self.name} in {self.vault.project.title}"
