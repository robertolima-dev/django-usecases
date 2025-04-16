from django.conf import settings
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from apps.ecommerce.documents import ProductDocument
from apps.ecommerce.models import Product

USE_ELASTIC = settings.PROJECT_ENV == "local"

if USE_ELASTIC:
    @receiver(post_save, sender=Product)
    def index_product(sender, instance, **kwargs):
        ProductDocument.update_or_create_document(instance)

    @receiver(post_delete, sender=Product)
    def delete_product(sender, instance, **kwargs):
        ProductDocument.delete_document(instance)
