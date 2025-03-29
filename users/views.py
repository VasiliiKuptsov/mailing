
import secrets

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.utils.crypto import get_random_string
from django.views.generic import CreateView, DeleteView, DetailView, FormView, ListView, TemplateView, UpdateView

from config.settings import EMAIL_HOST_USER
#from mailing_service.views import form_valid
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
        return form_valid(form)


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
            return reverse_lazy("mailing:index")

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
            return reverse_lazy("mailing:index")

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
        return form_valid(form)

'''

from django.shortcuts import render

from django.contrib.auth import login, get_user_model
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from django.views.generic import CreateView
import secrets
from users.forms import RegisterForm
from django.utils.http import urlsafe_base64_decode

from django.core.mail import send_mail
from users.management.commands.email_confirmation import send_confirmation_email
from config import settings
from django.shortcuts import render, redirect, get_object_or_404
from users.models import CustomUser
from django.urls import reverse_lazy, reverse


class RegisterView(CreateView):
    model = CustomUser
    form_class = RegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy("users:login")



    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token=token
        user.save()
        host=self.request.get_host()
        url=f'http://{host}/users/email_confirm/{token}/'
        send_mail(

            subject = 'Подтверждение',
            message = f'Привет! Перейли по ссылке {url}',
            from_email = settings.EMAIL_HOST_USER,
            recipient_list = [user.email]
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(CustomUser, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))

class LoginView(CreateView):
    def form_valid(self, form):
        user = form.get_user()
        if not user.is_active:
            form.add_error(None, "Ваш аккаунт заблокирован.")
            return self.form_invalid(form)
        login(self.request, user)
        return HttpResponseRedirect(self.get_success_url())


class ResetPasswordForm:
    pass


class PasswordReset(PasswordResetView):#ContextList
    form_class = PasswordResetForm
    template_name = 'users/register.html'
    success_url = '/reset_password'

    def form_valid(self, form):
        super().form_valid(form)
        return render(self.request, 'users/register.html',
                      super(PasswordReset, self).get_context_data())

# Create your views here.
'''