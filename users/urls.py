from django.contrib.auth.views import LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.services import block_user, email_verification
from users.views import (
    EmailConfirmationView,
    PasswordRecoveryView,
    UserCreateView,
    UserDeleteView,
    UserDetailView,
    UserListView,
    UserLoginView,
    UserUpdateView,
)

app_name = UsersConfig.name

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", UserCreateView.as_view(), name="register"),
    path("users/", UserListView.as_view(), name="users"),
    path("detail/<int:pk>/", UserDetailView.as_view(), name="detail"),
    path("update/<int:pk>/", UserUpdateView.as_view(), name="update"),
    path("delete/<int:pk>/", UserDeleteView.as_view(), name="delete"),
    path("email-confirm/<str:token>/", email_verification, name="email-confirm"),
    path(
        "email-confirmation/",
        EmailConfirmationView.as_view(),
        name="email_confirmation",
    ),
    path("password-recovery/", PasswordRecoveryView.as_view(), name="password_recovery"),
    path("block_user/<int:pk>", block_user, name="block_user"),
]
