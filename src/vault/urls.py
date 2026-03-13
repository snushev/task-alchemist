from django.urls import path
from . import views

urlpatterns = [
    path(
        "project/<int:pk>/add-secret/",
        views.SecretCreateView.as_view(),
        name="secret_create",
    ),
    path(
        "secret/<int:pk>/edit/", views.SecretUpdateView.as_view(), name="secret_update"
    ),
    path(
        "secret/<int:pk>/delete/",
        views.SecretDeleteView.as_view(),
        name="secret_delete",
    ),
]
