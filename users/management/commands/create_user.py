from django.contrib.auth.models import Group
from django.core.management import BaseCommand
from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        email = "users@coursecom"
        password = "1705"
        user = User.objects.create(email=email)
        user.set_password(password)
        user.is_active = True
        user.is_superuser = False
        user.is_staff = False
        users_group, created = Group.objects.get_or_create(name="Пользователи")
        user.groups.add(users_group)
        user.save()
        self.stdout.write(
            self.style.SUCCESS(
                f'Пользователь добавлен в группу "Пользователи"\nemail для входа: {email}\nпароль: {password}'
            )
        )
