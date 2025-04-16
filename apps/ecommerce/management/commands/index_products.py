from django.core.management.base import BaseCommand

from apps.ecommerce.documents import ProductDocument
from apps.ecommerce.models import Product


class Command(BaseCommand):
    help = "Indexa todos os produtos existentes no Elasticsearch"

    def handle(self, *args, **kwargs):
        products = Product.objects.all()
        count = 0

        for product in products:
            ProductDocument.update_or_create_document(product)
            self.stdout.write(self.style.SUCCESS(f"Indexado: {product.name}"))
            count += 1

        self.stdout.write(self.style.SUCCESS(f"✅ Total de produtos indexados: {count}")) # noqa501
