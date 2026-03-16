from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import (
    DetailView,
    CreateView,
    DeleteView,
    TemplateView,
)
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.cache import cache
from django.contrib.auth.decorators import login_required
from .models import Project, Task
from .forms import ProjectForm, TaskForm
from vault.models import Secret

# Create your views here.


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "projects/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        cache_key = f"user_stats_{user.id}"

        stats = cache.get(cache_key)
        if not stats:
            stats = {
                "total_projects": Project.objects.filter(owner=user).count(),
                "active_tasks": Task.objects.filter(
                    project__owner=user, is_completed=False
                ).count(),
                "total_secrets": Secret.objects.filter(
                    vault__project__owner=user
                ).count(),
            }
            cache.set(cache_key, stats, 300)

        context.update(stats)
        context["recent_projects"] = Project.objects.filter(owner=user).order_by("-id")[
            :5
        ]
        return context


class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = "projects/detail.html"
    context_object_name = "project"

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)


class ProjectCreateView(LoginRequiredMixin, CreateView):
    form_class = ProjectForm
    model = Project
    template_name = "projects/create.html"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.object.pk
        return reverse("project_detail", kwargs={"pk": pk})


class ProjectUpdateView(UserPassesTestMixin, UpdateView):
    model = Project
    fields = ["title", "description"]
    template_name = "projects/create.html"

    def get_success_url(self):
        return reverse("project_detail", kwargs={"pk": self.object.pk})

    def test_func(self):
        project = self.get_object()
        return self.request.user == project.owner


class ProjectDeleteView(UserPassesTestMixin, DeleteView):
    model = Project
    template_name = "projects/delete.html"

    def get_success_url(self):
        return reverse("dashboard")

    def test_func(self):
        project = self.get_object()
        return self.request.user == project.owner


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "projects/create_task.html"

    def form_valid(self, form):
        project_id = self.kwargs["pk"]
        project_obj = get_object_or_404(Project, pk=project_id, owner=self.request.user)

        form.instance.project = project_obj

        return super().form_valid(form)

    def get_success_url(self):
        pk = self.object.project.pk
        return reverse("project_detail", kwargs={"pk": pk})


class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    fields = ["title"]
    template_name = "projects/create_task.html"

    def get_success_url(self):
        return reverse("project_detail", kwargs={"pk": self.object.project.pk})

    def test_func(self):
        task = self.get_object()
        return self.request.user == task.project.owner


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    template_name = "projects/delete_task.html"

    def get_success_url(self):
        return reverse("project_detail", kwargs={"pk": self.object.project.pk})

    def test_func(self):
        task = self.get_object()
        return self.request.user == task.project.owner


def index_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    return render(request, "home.html")


@login_required
def task_toggle(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.is_completed = not task.is_completed
    task.save()
    return redirect("project_detail", pk=task.project.pk)
