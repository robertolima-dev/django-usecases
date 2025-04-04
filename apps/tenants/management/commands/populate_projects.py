import random

from django.core.management.base import BaseCommand
from faker import Faker

from apps.tenants.models import Project, Tenant

fake = Faker()


class Command(BaseCommand):
    help = 'Popula o banco com projetos de exemplo por tenant'

    def handle(self, *args, **kwargs):
        tenants = Tenant.objects.all()

        if not tenants.exists():
            self.stdout.write(self.style.ERROR("Nenhum tenant encontrado."))
            return

        total = 0
        for tenant in tenants:
            for _ in range(random.randint(3, 7)):
                Project.objects.create(
                    tenant=tenant,
                    name=fake.bs().title(),
                    description=fake.text(),
                    is_active=random.choice([True, False])
                )
                total += 1

        self.stdout.write(self.style.SUCCESS(f'{total} projetos criados com sucesso!')) # noqa501
