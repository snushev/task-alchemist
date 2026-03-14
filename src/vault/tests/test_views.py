from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from projects.models import Project
from ..models import Vault, Secret


class SecretCRUDTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="owner", password="password123")
        self.hacker = User.objects.create_user(
            username="hacker", password="password123"
        )

        self.project = Project.objects.create(title="My Project", owner=self.user)
        self.client.login(username="owner", password="password123")

    def test_vault_automatically_created(self):
        """Checks if signal works"""
        self.assertTrue(Vault.objects.filter(project=self.project).exists())

    def test_secret_create_view(self):
        """Tests create secret view"""
        url = reverse("secret_create", kwargs={"pk": self.project.pk})
        response = self.client.post(
            url, {"name": "DB_PASSWORD", "value": "topsecret123"}
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Secret.objects.count(), 1)
        self.assertEqual(Secret.objects.first().name, "DB_PASSWORD")

    def test_secret_security_other_user(self):
        """Checks if someone can add security to others projects"""
        self.client.login(username="hacker", password="password123")
        url = reverse("secret_create", kwargs={"pk": self.project.pk})
        response = self.client.post(url, {"name": "HACK", "value": "123"})

        self.assertEqual(response.status_code, 404)

    def test_secret_update_view(self):
        """Tests secrets edit"""
        secret = Secret.objects.create(
            vault=self.project.vault, name="Old", value="123"
        )
        url = reverse("secret_update", kwargs={"pk": secret.pk})

        response = self.client.post(url, {"name": "Updated", "value": "456"})
        secret.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(secret.name, "Updated")
