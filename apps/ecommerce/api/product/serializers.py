from rest_framework import serializers

from apps.ecommerce.models import Product


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ["id", "name", "stock", "price", "is_active", "owner"]
        read_only_fields = ["id", "owner"]
