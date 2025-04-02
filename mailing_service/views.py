from smtplib import SMTPException
from django.core.mail import send_mail
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin     #, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.views.generic import TemplateView
from config.settings import EMAIL_HOST_USER
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from django.urls import reverse_lazy
from django.utils import timezone
from mailing_service.forms import MailingForm, MessageForm, RecipientForm
from mailing_service.models import Mailing, AttemptMailing, Message, Recipient
from mailing_service.forms import ManagerMailingForm, OwnerMailingForm


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["count_recipients"] = Recipient.objects.all().count()
        context["recipients"] = Recipient.objects.all()
        context["count_all_mailings"] = Mailing.objects.all().count()
        context["all_mailings"] = Mailing.objects.all()
        context["active_mailings"] = Mailing.objects.filter(status=Mailing.STARTED)
        context["count_active_mailings"] = Mailing.objects.filter(
            status=Mailing.STARTED
        ).count()
        return context


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = "mailing/mailing_home.html"
    context_object_name = "mailings"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.groups.filter(name="managers").exists():
            context["is_in_group"] = self.request.user.groups.filter(
                name="managers"
            ).exists()
            context["all_mailings"] = (
                Mailing.objects.all().count()
                if Mailing.objects.all().count() > 0
                else 0
            )
            context["created_mailings"] = (
                Mailing.objects.filter(status=Mailing.CREATED).count()
                if Mailing.objects.filter().count() > 0
                else 0
            )
            context["active_mailings"] = (
                Mailing.objects.filter(status=Mailing.STARTED).count()
                if Mailing.objects.filter().count() > 0
                else 0
            )
            context["ended_mailings"] = (
                Mailing.objects.filter(status=Mailing.ENDED).count()
                if Mailing.objects.filter().count() > 0
                else 0
            )

        elif user.groups.filter(name="users").exists():
            context["all_mailings"] = (
                Mailing.objects.filter(owner=user).count()
                if Mailing.objects.filter(owner=user).count() > 0
                else 0
            )
            logging.debug(context["all_mailings"])
            context["created_mailings"] = (
                Mailing.objects.filter(owner=user, status=Mailing.CREATED).count()
                if Mailing.objects.filter(owner=user).count() > 0
                else 0
            )
            context["active_mailings"] = (
                Mailing.objects.filter(owner=user, status=Mailing.STARTED).count()
                if Mailing.objects.filter(owner=user).count() > 0
                else 0
            )
            context["ended_mailings"] = (
                Mailing.objects.filter(owner=user, status=Mailing.ENDED).count()
                if Mailing.objects.filter(owner=user).count() > 0
                else 0
            )
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        active_mailings = Mailing.objects.filter(status=Mailing.STARTED)
        active_attempt_mailings = AttemptMailing.objects.filter(
            mailing__in=active_mailings
        )
        for attempt_mailing in active_attempt_mailings:
            if attempt_mailing.date_attempt.date() < timezone.now().date():
                mailing = attempt_mailing.mailing
                mailing.status = Mailing.ENDED
                mailing.save()

        return queryset


class MailingCreateView(CreateView):
    model = Mailing
    template_name = "mailing/mailing_create.html"
    form_class = OwnerMailingForm
    success_url = reverse_lazy("mailing_service:mailing_home")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class MailingUpdateView(UpdateView):
    model = Mailing
    template_name = "mailing/create_update_mailing_create.html"
    success_url = reverse_lazy("mailing_service:mailing_home")


class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = "mailing/mailing_delete.html"
    context_object_name = "mailing"
    success_url = reverse_lazy("mailing_service:mailing_home")


class MessageListView(ListView):
    model = Message
    template_name = "message/message_home.html"
    context_object_name = "messages"
    success_url = reverse_lazy("mailing_service:message_delete")


class MessageCreateView(LoginRequiredMixin, CreateView):  # UserPassesTestMixin,
    model = Message
    template_name = "message/create_update_message.html"
    fields = ["subject_letter", "body_letter"]
    success_url = reverse_lazy("mailing_service:message_home")

    def form_valid(self, form):
        recipient = form.save()
        recipient.owner = self.request.user
        recipient.save()
        return super().form_valid(form)


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    template_name = "message/message_detail.html"
    context_object_name = "message"

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if not self.request.user.is_superuser:
            raise PermissionDenied
        return self.object


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    fields = ["subject_letter", "body_letter"]
    template_name = "message/create_update_message.html"
    success_url = reverse_lazy("mailing_service:message_home")

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if not self.request.user.is_superuser:
            raise PermissionDenied
        return self.object


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = "message/message_delete.html"
    context_object_name = "message"
    success_url = reverse_lazy("mailing_service:message_home")

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if not self.request.user.is_superuser:
            raise PermissionDenied
        return self.object


class RecipientListView(ListView):
    model = Recipient
    template_name = "recipient/recipient_home.html"
    context_object_name = "recipients"


class RecipientDetailView(LoginRequiredMixin, DetailView):
    model = Recipient
    form_class = RecipientForm

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user.is_superuser or self.request.user.groups.filter(name="Менеджеры"):
            return self.object
        if self.object.owner != self.request.user and not self.request.user.is_superuser:
            raise PermissionDenied
        return self.object


class RecipientCreateView(LoginRequiredMixin, CreateView): # UserPassesTestMixin,
    model = Recipient
    template_name = "recipient/create_update_recipient.html"
    fields = ["email", "fullname", "comment"]
    success_url = reverse_lazy("mailing_service:recipient_home")


class RecipientUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipient
    fields = ["email", "fullname", "comment"]
    template_name = "recipient/create_update_recipient.html"
    success_url = reverse_lazy("mailing_service:recipient_home")

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_superuser:
            raise PermissionDenied
        return self.object


class RecipientDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipient
    template_name = "recipient/recipient_delete.html"
    context_object_name = "recipient"
    success_url = reverse_lazy("mailing_service:recipient_home")

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_superuser:
            raise PermissionDenied
        return self.object


class AttemptMailingListView(LoginRequiredMixin, ListView):
    model = AttemptMailing
    template_name = "attempt/attempt_mailing_home.html"
    context_object_name = "attempts"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.groups.filter(name="users").exists():
            started_mailings = Mailing.objects.filter(
                status=Mailing.STARTED, owner=self.request.user
            )

            context["started_mailings"] = (
                AttemptMailing.objects.filter(
                    mailing__in=started_mailings, owner=self.request.user
                ).count()
                if AttemptMailing.objects.filter(
                    mailing__in=started_mailings, owner=self.request.user
                ).count()
                > 0
                else 0
            )

            context["count_attempts_mailings"] = (
                AttemptMailing.objects.filter(owner=self.request.user).count()
                if AttemptMailing.objects.filter(owner=self.request.user).count() > 0
                else 0
            )

            context["count_success_attempts_mailings"] = (
                AttemptMailing.objects.filter(
                    status=AttemptMailing.SUCCESS, owner=self.request.user
                ).count()
                if AttemptMailing.objects.filter(
                    status=AttemptMailing.SUCCESS, owner=self.request.user
                ).count()
                > 0
                else 0
            )

            context["count_not_success_attempts_mailings"] = (
                AttemptMailing.objects.filter(
                    status=AttemptMailing.NOT_SUCCESS, owner=self.request.user
                ).count()
                if AttemptMailing.objects.filter(
                    status=AttemptMailing.NOT_SUCCESS, owner=self.request.user
                ).count()
                > 0
                else 0
            )

        elif user.groups.filter(name="managers").exists():
            context["is_in_group"] = self.request.user.groups.filter(
                name="managers"
            ).exists()
            started_mailings = Mailing.objects.filter(status=Mailing.STARTED)

            context["started_mailings"] = (
                AttemptMailing.objects.filter(mailing__in=started_mailings).count()
                if AttemptMailing.objects.filter(mailing__in=started_mailings).count()
                > 0
                else 0
            )

            context["count_attempts_mailings"] = (
                AttemptMailing.objects.all().count()
                if AttemptMailing.objects.all().count() > 0
                else 0
            )

            context["count_success_attempts_mailings"] = (
                AttemptMailing.objects.filter(
                    status=AttemptMailing.SUCCESS,
                ).count()
                if AttemptMailing.objects.filter(status=AttemptMailing.SUCCESS).count()
                > 0
                else 0
            )

            context["count_not_success_attempts_mailings"] = (
                AttemptMailing.objects.filter(status=AttemptMailing.NOT_SUCCESS).count()
                if AttemptMailing.objects.filter(
                    status=AttemptMailing.NOT_SUCCESS
                ).count()
                > 0
                else 0
            )
        return context


class AttemptMailingCreateView(LoginRequiredMixin, CreateView):
    model = AttemptMailing
    success_url = reverse_lazy("mailing_service:mailing_home")
    fields = ["mailing"]

    def form_valid(self, form, recipient=None):
        """Send a main email"""
        form.instance.owner = self.request.user
        mailing_id = self.request.POST.get("mailing")
        mailing_instance = Mailing.objects.get(id=mailing_id)
        try:
            if mailing_instance.is_active:
                send_mail(
                    mailing_instance.message.subject_letter,
                    mailing_instance.message.body_letter,
                    from_email=EMAIL_HOST_USER,
                    recipient_list=[Recipient(id).email],
                    fail_silently=False,
                )
                AttemptMailing.objects.create(
                    date_attempt=timezone.now(),
                    status=AttemptMailing.SUCCESS,
                    answer="успешно отпралено",
                    mailing=mailing_instance,
                    owner=self.request.user,
                )
                if not mailing_instance.status == Mailing.STARTED:
                    mailing_instance.status = Mailing.STARTED
                    mailing_instance.save()
                return render(self.request, "attempt/attempt_good_create.html")
            else:
                return render(self.request, "attempt/attempt_bad_create.html")
        except SMTPException as e:
            AttemptMailing.objects.create(
                date_attempt=timezone.now(),
                status=AttemptMailing.NOT_SUCCESS,
                answer=e,
                mailing=mailing_instance,
            )
            return render(self.request, "attempt/attempt_bad_create.html")