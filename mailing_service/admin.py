from django.contrib import admin

# Register your models here.
from django.contrib import admin

from mailing_service.models import Mailing, AttemptMailing, Message, Recipient
from users.models import User


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ("id", "fullname", "email", "comment", "owner")
    list_filter = ("fullname",)
    search_fields = (
        "fullname",
        "email",
    )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "subject_letter",
        "body_letter",
        "owner",
    )
    search_fields = ("subject_letter",)
    list_filter = ("subject_letter",)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ("id", "first_sending", "last_sending", "status", "message", "owner")
    search_fields = ("status",)
    list_filter = ("status",)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "avatar",
        "email",
        "first_name",
        "last_name",
        "middle_name",
        "phone_number",
    )
    search_fields = ("email",)
    list_filter = ("email",)


@admin.register(AttemptMailing)
class AttemptMailingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "owner",
        "date_attempt",
        "status",
    )
    search_fields = ("owner",)
    list_filter = ("owner",)
