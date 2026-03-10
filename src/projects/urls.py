from os import name
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.ProjectListView.as_view(), name="projects"),
    path("<int:pk>/", views.ProjectDetailView.as_view(), name="project_detail"),
    path("create/", views.ProjectCreateView.as_view(), name="project_create"),
    path("<int:pk>/edit/", views.ProjectUpdateView.as_view(), name="project_edit"),
    path("<int:pk>/delete/", views.ProjectDeleteView.as_view(), name="project_delete"),
]
