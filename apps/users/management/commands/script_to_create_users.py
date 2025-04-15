from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from faker import Faker

User = get_user_model()
fake = Faker("pt_BR")


class Command(BaseCommand):
    help = "Cadastra 100 usuarios"

    def handle(self, *args, **kwargs):

        for i in list(range(1, 100)):
            user, _ = User.objects.get_or_create(
                username=fake.user_name(),
                defaults={
                    "email": fake.email(),
                    "password": "123456",
                    "first_name": fake.first_name(),
                    "last_name": fake.last_name()
                },
            )
            print(user)
            print('')
