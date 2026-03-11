from os import name
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.ProjectListView.as_view(), name="projects"),
    path("create/", views.ProjectCreateView.as_view(), name="project_create"),
    path(
        "<int:pk>/",
        include(
            [
                path("", views.ProjectDetailView.as_view(), name="project_detail"),
                path("edit/", views.ProjectUpdateView.as_view(), name="project_edit"),
                path(
                    "delete/", views.ProjectDeleteView.as_view(), name="project_delete"
                ),
                path(
                    "task/create/", views.TaskCreateView.as_view(), name="task_create"
                ),
            ],
        ),
    ),
    path("task/<int:pk>/update", views.TaskUpdateView.as_view(), name="task_update"),
    path("task/<int:pk>/delete", views.TaskDeleteView.as_view(), name="task_delete"),
]
