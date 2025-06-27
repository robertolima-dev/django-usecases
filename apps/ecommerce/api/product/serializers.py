from rest_framework import serializers

from apps.ecommerce.models import Product


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ["id", "name", "description", "stock", "price", "is_active", "owner", "created_at",]  # noqa: E501
        read_only_fields = ["id", "owner"]


class ProductCustomSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    stock = serializers.IntegerField(read_only=True)
    price = serializers.FloatField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    owner = serializers.JSONField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
