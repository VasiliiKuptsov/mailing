from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from config.settings import CACHE_ENABLE, EMAIL_HOST_USER
from mailing.models import Mailing, AttemptMailing


def run_mailing(request, pk):
    """Функция запуска рассылки по требованию"""
    mailing = get_object_or_404(Mailing, id=pk)
    for recipient in mailing.recipients.all():
        try:
            mailing.status = Mailing.LAUNCHED
            send_mail(
                subject=mailing.message.subject_letter,
                message=mailing.message.body_letter,
                from_email=EMAIL_HOST_USER,
                recipient_list=[recipient.email],
                fail_silently=False,
            )
            AttemptMailing.objects.create(
                date_attempt=timezone.now(),
                status=AttemptMailing.STATUS_OK,
                answer="Email отправлен",
                mailing=mailing,
            )
        except Exception as e:
            print(f"Ошибка при отправке письма для {recipient.email}: {str(e)}")
            AttemptMailing.objects.create(
                date_attempt=timezone.now(),
                status=AttemptMailing.STATUS_NOK,
                answer=str(e),
                mailing=mailing,
            )
    if mailing.end_sending and mailing.end_sending <= timezone.now():
        # Если время рассылки закончилось, обновляем статус на "завершено"
        mailing.status = Mailing.COMPLETED
    mailing.save()
    return redirect("mailing_service:mailing_home")


def get_mailing_from_cache():
    """Получение данных по рассылкам из кэша, если кэш пуст берем из БД."""
    if not CACHE_ENABLE:
        return Mailing.objects.all()
    key = "mailing_list"
    cache_data = cache.get(key)
    if cache_data is not None:
        return cache_data
    cache_data = Mailing.objects.all()
    cache.set(key, cache_data)
    return cache_data


def get_attempt_from_cache():
    """Получение данных по попыткам из кэша, если кэш пуст берем из БД."""
    if not CACHE_ENABLE:
        return AttemptMailing.objects.all()
    key = "attempt_list"
    cache_data = cache.get(key)
    if cache_data is not None:
        return cache_data
    cache_data = AttemptMailing.objects.all()
    cache.set(key, cache_data)
    return cache_data


@login_required
def block_mailing(request, pk):
    mailing = Mailing.objects.get(pk=pk)
    mailing.is_active = {mailing.is_active: False, not mailing.is_active: True}[True]
    mailing.save()
    return redirect(reverse("mailing_service:mailing_home"))