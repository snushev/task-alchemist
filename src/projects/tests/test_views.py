from django.test import TestCase
from django.urls import reverse
from ..models import Project, Task


class ProjectViewTest(TestCase):
    def test_dashboard_access(self):
        url = reverse("projects")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_context_response(self):

        Project.objects.create(title="title", description="description")
        Project.objects.create(title="title2", description="description")

        response = self.client.get("/projects/")
        self.assertEqual(response.context["projects"].count(), 2)
