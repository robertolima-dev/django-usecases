from rest_framework import serializers

from apps.ecommerce.models import Product


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ["id", "name", "description", "stock", "price", "is_active", "owner"] # noqa501
        read_only_fields = ["id", "owner"]
