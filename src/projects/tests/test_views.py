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


class ProjectDetailTest(TestCase):
    def test_detail_access(self):
        project = Project.objects.create(title="t", description="desc")
        url = reverse("project_detail", kwargs={"pk": project.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_tasks_list(self):
        project = Project.objects.create(title="t", description="d")
        Task.objects.create(project=project, title="test")
        Task.objects.create(project=project, title="test2")

        url = reverse("project_detail", kwargs={"pk": project.pk})
        response = self.client.get(url)
        self.assertEqual(response.context["project"].tasks.count(), 2)
