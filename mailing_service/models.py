from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import CharField, DateTimeField, ForeignKey, ManyToManyField, TextField
from users.models import User

NULLABLE = {"blank": True, "null": True}


class Recipient(models.Model):
    email = models.EmailField(max_length=255, unique=True, verbose_name="E-mail")
    fullname = CharField(max_length=100)
    comment = TextField(verbose_name="комментарий")
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, **NULLABLE, verbose_name="Владелец")

    def __str__(self):
        return f"{self.fullname}"

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
        ordering = ["email", "fullname"]


class Message(models.Model):
    subject_letter = CharField(max_length=100, unique=True, verbose_name="тема")
    body_letter = TextField(verbose_name="комментарий")
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, **NULLABLE, verbose_name="Владелец")

    class Meta:
        verbose_name = "Письмо"
        verbose_name_plural = "Письма"
        ordering = ["subject_letter", "body_letter"]

    def __str__(self):
        return self.subject_letter


class Mailing(models.Model):
    CREATED = "cоздана"
    STARTED = "запущена"
    ENDED = "завершена"

    STATUS_IN_CHOICES = [
        (CREATED, "Создана"),
        (STARTED, "Запущена"),
        (ENDED, "Завершена"),
    ]

    first_sending = DateTimeField(
        verbose_name="Время начала", auto_now_add=True, editable=False
    )
    last_sending = DateTimeField(
        verbose_name="Время конца", auto_now_add=True, editable=False
    )
    status = CharField(
        choices=STATUS_IN_CHOICES,
        max_length=10,
        verbose_name="Статус",
        default=CREATED,
        editable=False,
    )
    message = ForeignKey(Message, on_delete=models.CASCADE, verbose_name="Письмо")
    recipient = ManyToManyField(
        Recipient, related_name="mailings", verbose_name="Клиент"
    )
    is_active = models.BooleanField(default=True, verbose_name="активна")
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, **NULLABLE, verbose_name="Владелец")

    def __str__(self):
        return f"Рассылка {self.id}"

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = ["first_sending", "last_sending", "status"]
        permissions = [
            ("can_disable_mailing", "Возможность отключения рассылки"),
        ]


class AttemptMailing(models.Model):
    SUCCESS = "Успешно"
    NOT_SUCCESS = "Не успешно"

    STATUS_IN_CHOICES = [
        (SUCCESS, "Успешно"),
        (NOT_SUCCESS, "Не успешно"),
    ]

    date_attempt = DateTimeField(
        verbose_name="Дата и время попытки", auto_now_add=True, editable=False
    )
    status = CharField(
        choices=STATUS_IN_CHOICES, max_length=11, verbose_name="Статус", editable=False
    )
    answer = TextField(verbose_name="Ответ почтового сервера", editable=False)
    mailing = ForeignKey(
        Mailing,
        related_name="mailing",
        verbose_name="Рассылка",
        on_delete=models.CASCADE,
    )
    owner = models.ForeignKey(
        get_user_model(),
        verbose_name='Владелец',
        help_text='Укажите продавца товара',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return f"{self.date_attempt} <{self.status}>"

    class Meta:
        verbose_name = "Попытка"
        verbose_name_plural = "Попытки"
        ordering = ["date_attempt", "status", "answer", "mailing"]



