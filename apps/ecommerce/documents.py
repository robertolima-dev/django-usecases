from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from apps.ecommerce.models import Product


@registry.register_document
class ProductDocument(Document):
    owner = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'username': fields.TextField(),
        'email': fields.TextField(),
    })

    class Index:
        name = "products"

    class Django:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "price",
            "stock",
            "image",
            "category",
            "is_active",
            "created_at",
        ]

    @classmethod
    def update_or_create_document(cls, product: Product):
        cls().update(product)

    @classmethod
    def delete_document(cls, product: Product):
        cls().delete(product)
