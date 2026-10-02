from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView
from django.views.generic import ListView, FormView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.conf import settings

from django.contrib.auth.models import User
from django.contrib.auth.forms import BaseUserCreationForm
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin

from django.core.exceptions import ValidationError
import markdown2

from .models import BorgRepository, Voucher
from .forms import BorgRepositoryForm, RegisterUserForm, DeleteUserForm


class UserOwnsRepositoryMixin(UserPassesTestMixin):
    def test_func(self):
        repo = get_object_or_404(BorgRepository, pk=self.kwargs["pk"])
        return repo.user == self.request.user


class LoginView(TemplateView):
    template_name = "login.html"


class LandingView(TemplateView):
    template_name = "landing.html"


class MarkdownView(TemplateView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        source = (settings.MARKDOWN_PAGE_DIR / self.md).read_text()
        context["markdown_content"] = markdown2.markdown(source)
        return context


class DataProtectionView(MarkdownView):
    template_name = "markdown.html"
    md = "dataprotection.md"


class ImprintView(MarkdownView):
    template_name = "markdown.html"
    md = "imprint.md"


class BorgView(LoginRequiredMixin, ListView):
    template_name = "borg_list.html"
    content_object_name = "borg_repositories"

    def get_queryset(self):
        data = BorgRepository.objects.filter(user=self.request.user)
        return data


class RegisterUserView(FormView):
    template_name = "register.html"
    form_class = RegisterUserForm
    success_url = "/"

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class DeleteUserView(LoginRequiredMixin, FormView):
    template_name = "delete.html"
    form_class = DeleteUserForm
    success_url = "/"

    def form_valid(self, form):
        user = self.request.user
        user.delete()
        return super().form_valid(form)


class BorgRepositoryCreateView(LoginRequiredMixin, CreateView):
    model = BorgRepository
    success_url = "/borg/"
    form_class = BorgRepositoryForm

    def get_initial(self):
        return {"user": self.request.user}

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class BorgRepositoryDeleteView(LoginRequiredMixin, UserOwnsRepositoryMixin, DeleteView):
    model = BorgRepository
    success_url = "/borg/"


class BorgRepositoryUpdateView(LoginRequiredMixin, UserOwnsRepositoryMixin, UpdateView):
    model = BorgRepository
    success_url = "/borg/"
    form_class = BorgRepositoryForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
