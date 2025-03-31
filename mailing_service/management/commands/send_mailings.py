from django.core.mail import send_mail
from django.core.management import BaseCommand
from django.utils import timezone

from config.settings import EMAIL_HOST_USER
from mailing.models import Mailing, AttemptMailing


class Command(BaseCommand):
    help = "Отправка почтовых отправлений получателям"

    def handle(self, *args, **kwargs):
        mailings = Mailing.objects.filter(status__in=[Mailing.CREATED, Mailing.LAUNCHED])
        for mailing in mailings:
            for recipient in mailing.recipients.all():
                try:
                    send_mail(
                        mailing.message.subject_letter,
                        mailing.message.body_letter,
                        from_email=EMAIL_HOST_USER,
                        recipient_list=[recipient.email],
                        fail_silently=False,
                    )
                    MailingAttempt.objects.create(
                        date_attempt=timezone.now(),
                        status=AttemptMailing.STATUS_OK,
                        answer="Email отправлен",
                        mailing=mailing,
                    )
                    print(f"Сообщение {mailing.message.subject_letter} успешно отправлено на  {recipient.email}")
                except Exception as e:
                    MailingAttempt.objects.create(
                        date_attempt=timezone.now(),
                        status=AttemptMailing.STATUS_NOK,
                        answer=str(e),
                        mailing=mailing,
                    )
                    print(str(e))
            mailing.save()