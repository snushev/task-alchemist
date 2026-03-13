from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from .models import Vault, Secret


class SecretCreateView(LoginRequiredMixin, CreateView):
    model = Secret
    fields = ["name", "value"]
    template_name = "vault/secret_form.html"

    def form_valid(self, form):
        vault = get_object_or_404(
            Vault,
            project__pk=self.kwargs["pk"],
            project__owner=self.request.user,
        )
        form.instance.vault = vault
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("project_detail", kwargs={"pk": self.kwargs["pk"]})


class SecretUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Secret
    fields = ["name", "value"]
    template_name = "vault/secret_form.html"

    def test_func(self):
        secret = self.get_object()
        return self.request.user == secret.vault.project.owner

    def get_success_url(self):
        return reverse("project_detail", kwargs={"pk": self.object.vault.project.pk})


class SecretDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Secret
    template_name = "vault/secret_confirm_delete.html"

    def test_func(self):
        secret = self.get_object()
        return self.request.user == secret.vault.project.owner

    def get_success_url(self):
        return reverse("project_detail", kwargs={"pk": self.object.vault.project.pk})
