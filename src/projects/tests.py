from django.test import TestCase
from .models import Project, Task
from django.utils import timezone
# Create your tests here.


class ProjectTest(TestCase):
    def setUp(self):
        self.project = Project.objects.create(title="test", description="some desc")

    def test_project_title(self):
        self.assertEqual(self.project.title, "test")

    def test_project_created_at(self):
        self.assertIsNotNone(self.project.created_at)
        self.assertTrue(isinstance(self.project.created_at, timezone.datetime))


class TaskTest(TestCase):
    def setUp(self):
        project = Project.objects.create(title="test", description="some desc")
        self.task = Task.objects.create(
            project=project, title="test", is_completed=False
        )

    def test_task_project(self):
        self.assertEqual(self.task.project.title, self.project.title)
