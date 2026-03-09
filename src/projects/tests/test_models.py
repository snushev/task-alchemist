from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
from ..models import Project, Task


class ProjectTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testomir_project")
        self.project = Project.objects.create(
            title="test", description="some desc", owner=self.user
        )

    def test_project_title(self):
        self.assertEqual(self.project.title, "test")

    def test_project_created_at(self):
        self.assertIsNotNone(self.project.created_at)
        self.assertTrue(isinstance(self.project.created_at, timezone.datetime))


class TaskTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testomir_task")

    def create_project(self, title="test"):
        return Project.objects.create(title=title, description="desc", owner=self.user)

    def create_task(self, project, title="task"):
        return Task.objects.create(project=project, title=title)

    def test_task_project(self):
        project = self.create_project()
        task = self.create_task(project=project)
        self.assertEqual(task.project.title, project.title)

    def test_multiple_tasks_for_a_project(self):
        project = self.create_project()
        self.create_task(project=project, title="t1")
        self.create_task(project=project, title="t2")
        self.create_task(project=project, title="t3")
        self.assertEqual(project.tasks.count(), 3)

    def test_cascade_delete(self):
        project = self.create_project()
        self.create_task(project=project)
        project.delete()
        self.assertEqual(Task.objects.count(), 0)
