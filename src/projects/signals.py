from django.db.models.signals import post_save
from django.dispatch import receiver
from vault.models import Vault


@receiver(post_save, sender="projects.Project")
def create_project_vault(sender, instance, created, **kwargs):
    if created:
        Vault.objects.create(project=instance)
