from django.urls import path
from . import views

urlpatterns = [
    path("", views.DashboardView.as_view(), name="dashboard"),
    path("create/", views.ProjectCreateView.as_view(), name="project_create"),
    path(
        "<int:pk>/dashboard/", views.ProjectDetailView.as_view(), name="project_detail"
    ),
    path("<int:pk>/edit/", views.ProjectUpdateView.as_view(), name="project_update"),
    path("<int:pk>/delete/", views.ProjectDeleteView.as_view(), name="project_delete"),
    path("<int:pk>/task/create/", views.TaskCreateView.as_view(), name="task_create"),
    path("task/<int:pk>/update/", views.TaskUpdateView.as_view(), name="task_update"),
    path("task/<int:pk>/delete/", views.TaskDeleteView.as_view(), name="task_delete"),
    path("task/<int:pk>/toggle/", views.task_toggle, name="task_toggle"),
]
