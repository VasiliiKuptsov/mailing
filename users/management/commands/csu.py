from django.core.management import BaseCommand
from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        email = "admin@course.com"
        password = "1705"
        user = User.objects.create(email=email)
        user.set_password(password)
        user.is_active = True
        user.is_superuser = True
        user.is_staff = True
        user.save()
        self.stdout.write(self.style.SUCCESS(f"Создан администратор\nemail для входа: {email}\nпароль: {password}"))
