from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Project, Task
from .forms import ProjectForm, TaskForm

# Create your views here.


class ProjectListView(ListView):
    model = Project
    template_name = "projects/list.html"
    context_object_name = "projects"


class ProjectDetailView(DetailView):
    model = Project
    template_name = "projects/detail.html"
    context_object_name = "project"


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
        return reverse("projects")

    def test_func(self):
        project = self.get_object()
        return self.request.user == project.owner
