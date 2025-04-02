
import secrets

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.utils.crypto import get_random_string
from django.views.generic import CreateView, DeleteView, DetailView, FormView, ListView, TemplateView, UpdateView
from config.settings import EMAIL_HOST_USER
from users.forms import PasswordRecoveryForm, UserLoginForm, UserRegistrationForm, UserUpdateForm
from users.models import User


class UserCreateView(CreateView):
    model = User
    form_class = UserRegistrationForm
    success_url = reverse_lazy("users:email_confirmation")

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        host = self.request.get_host()
        url = f"http://{host}/users/email-confirm/{token}/"
        user.token = token
        user.save()
        send_mail(
            subject="Подтверждение почты",
            message=f"Здравствуйте, перейдите по ссылке для подтверждения почты: {url} ",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


class UserLoginView(LoginView):
    model = User
    form_class = UserLoginForm


class UserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    template_name = "users/user_list.html"

    def test_func(self):
        return self.request.user.groups.filter(name="Менеджеры").exists() or self.request.user.is_superuser


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    form_class = UserUpdateForm

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user.is_superuser:
            return self.object
        raise PermissionDenied


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm

    def get_success_url(self):
        if self.request.user.is_superuser:
            return reverse_lazy("users:users")
        else:
            return reverse_lazy("mailing:home")

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if not self.request.user.is_superuser:
            raise PermissionDenied
        return self.object


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User

    def get_success_url(self):
        if self.request.user.is_superuser:
            return reverse_lazy("users:users")
        else:
            return reverse_lazy("mailing:home")

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if not self.request.user.is_superuser:
            raise PermissionDenied
        return self.object


class EmailConfirmationView(TemplateView):
    model = User
    template_name = "users/email_confirmation.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Письмо активации отправлено"
        return context


class PasswordRecoveryView(FormView):
    template_name = "users/password_recovery.html"
    form_class = PasswordRecoveryForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        user = User.objects.get(email=email)
        length = 12
        alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        password = get_random_string(length, alphabet)
        user.set_password(password)
        user.save()
        send_mail(
            subject="Восстановление пароля",
            message=f"Ваш новый пароль: {password}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )
        return super().form_valid(form)
