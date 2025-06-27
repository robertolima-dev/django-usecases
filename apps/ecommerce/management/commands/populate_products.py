import random
from decimal import Decimal

from django.core.management.base import BaseCommand
from faker import Faker

from apps.ecommerce.models import Product

fake = Faker()


class Command(BaseCommand):
    help = "Popula o banco com produtos fake para testes no módulo de pedidos."  # noqa: E501

    def handle(self, *args, **kwargs):
        num_products = 100
        created = []

        for _ in range(num_products):
            product = Product.objects.create(
                name=fake.unique.word().capitalize(),
                description=fake.sentence(nb_words=12),
                price=Decimal(random.uniform(10.0, 500.0)).quantize(Decimal("0.01")),  # noqa: E501
                stock=random.randint(1, 100)
            )
            created.append(product)

        self.stdout.write(self.style.SUCCESS(f"{len(created)} produtos criados com sucesso."))  # noqa: E501
