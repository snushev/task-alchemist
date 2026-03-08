from typing import override
from django.db import models

# Create your models here.


class Project(models.Model):
    title: str = models.CharField(max_length=50)
    description: str = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    @override
    def __str__(self) -> str:
        return self.title
