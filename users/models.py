

from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    username = None #models.CharField(null=True, blank=True)
    email = models.EmailField(unique=True, verbose_name="Email")
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    middle_name = models.CharField(max_length=50, verbose_name="Отчество", null=True, blank=True)
    phone_number = models.CharField(
        max_length=20, verbose_name="Номер телефона", null=True, blank=True, help_text="Введите номер телефона"
    )
    #is_active = BooleanField(default=False)
    avatar = models.ImageField(upload_to="users/avatars", null=True, blank=True, verbose_name="Аватар")
    token = models.CharField(max_length=70, unique=True, verbose_name='token', blank=True, null=True )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email

