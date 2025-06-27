from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from faker import Faker

from apps.tenants.models import Tenant

fake = Faker()
User = get_user_model()


class Command(BaseCommand):
    help = 'Popula o banco com tenants e usuários de exemplo'

    def handle(self, *args, **kwargs):
        for _ in range(3):

            owner_email = fake.unique.email()
            owner = User.objects.create_user(
                username=owner_email,
                email=owner_email,
                password='123456'
            )

            tenant = Tenant.objects.create(
                name=fake.company(),
                domain=fake.domain_name(),
                owner=owner
            )
            tenant.users.add(owner)

            for _ in range(2):  # cria 2 usuários extras por tenant
                email = fake.unique.email()
                user = User.objects.create_user(
                    username=email,
                    email=email,
                    password='123456'
                )
                tenant.users.add(user)

        self.stdout.write(self.style.SUCCESS('Tenants e usuários criados com sucesso!'))  # noqa: E501
