from django.test import TestCase
from django.contrib.auth.models import User
from projects.models import Project
from ..models import Vault, Secret


class VaultModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testomir")
        self.project = Project.objects.create(
            title="T", description="D", owner=self.user
        )

    def test_vault_creation(self):
        vault = Vault.objects.create(project=self.project)
        self.assertEqual(vault.project.title, "T")

        from django.db import IntegrityError

        with self.assertRaises(IntegrityError):
            Vault.objects.create(project=self.project)


class SecretModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testomir")
        self.project = Project.objects.create(
            title="T", description="D", owner=self.user
        )
        self.vault = Vault.objects.create(project=self.project)

    def test_adding_secrets_to_vault(self):
        Secret.objects.create(vault=self.vault, name="secret", value="1234243")
        Secret.objects.create(vault=self.vault, name="secret1", value="1234243")

        self.assertEqual(self.vault.secrets.count(), 2)
