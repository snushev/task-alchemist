from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Project, Task


class ProjectViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="view_user")

    def test_dashboard_access(self):
        url = reverse("projects")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_context_response(self):

        Project.objects.create(
            title="title", description="description", owner=self.user
        )
        Project.objects.create(
            title="title2", description="description", owner=self.user
        )

        response = self.client.get("/projects/")
        self.assertEqual(response.context["projects"].count(), 2)


class ProjectDetailTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="detail_user")

    def test_detail_access(self):
        project = Project.objects.create(title="t", description="desc", owner=self.user)
        url = reverse("project_detail", kwargs={"pk": project.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_tasks_list(self):
        project = Project.objects.create(title="t", description="d", owner=self.user)
        Task.objects.create(project=project, title="test")
        Task.objects.create(project=project, title="test2")

        url = reverse("project_detail", kwargs={"pk": project.pk})
        response = self.client.get(url)
        self.assertEqual(response.context["project"].tasks.count(), 2)
