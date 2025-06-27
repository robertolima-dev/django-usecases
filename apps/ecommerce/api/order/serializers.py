from rest_framework import serializers

from apps.ecommerce.models import Order, Product


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    product = serializers.StringRelatedField(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source="product", write_only=True
    )

    class Meta:
        model = Order
        fields = ["id", "user", "product", "product_id", "quantity", "paid", "created_at"]  # noqa: E501
        read_only_fields = ["user", "paid", "created_at"]
