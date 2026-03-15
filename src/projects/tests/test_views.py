from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Project, Task


class ProjectViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="view_user", password="password123"
        )
        self.client.login(username="view_user", password="password123")

    def test_dashboard_access(self):
        url = reverse("dashboard")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_context_response(self):
        Project.objects.create(
            title="title", description="description", owner=self.user
        )
        Project.objects.create(
            title="title2", description="description", owner=self.user
        )
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.context["recent_projects"].count(), 2)


class ProjectDetailTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="detail_user", password="password123"
        )
        self.client.login(username="detail_user", password="password123")

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


class ProjectCreateTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="creator", password="password123")
        self.client.login(username="creator", password="password123")

    def test_project_create_post(self):
        url = reverse("project_create")
        data = {"title": "New Project", "description": "Success!"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Project.objects.count(), 1)
        self.assertEqual(Project.objects.first().owner, self.user)


class ProjectSecurityTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="123")
        self.user2 = User.objects.create_user(username="user2", password="123")
        self.project1 = Project.objects.create(title="User1 Project", owner=self.user1)

    def test_unauthorized_update(self):
        self.client.login(username="user2", password="123")
        url = reverse("project_edit", kwargs={"pk": self.project1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_project_delete_post(self):
        self.client.login(username="user1", password="123")
        url = reverse("project_delete", kwargs={"pk": self.project1.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Project.objects.filter(pk=self.project1.pk).count(), 0)


class TaskViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tasker", password="password123")
        self.other_user = User.objects.create_user(
            username="hacker", password="password123"
        )
        self.project = Project.objects.create(title="My Project", owner=self.user)
        self.client.login(username="tasker", password="password123")

    def test_task_create_post(self):
        url = reverse("task_create", kwargs={"pk": self.project.pk})
        data = {"title": "New Task"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.count(), 1)

    def test_task_create_security(self):
        self.client.login(username="hacker", password="password123")
        url = reverse("task_create", kwargs={"pk": self.project.pk})
        response = self.client.post(url, {"title": "I am a hacker"})
        self.assertEqual(response.status_code, 404)
