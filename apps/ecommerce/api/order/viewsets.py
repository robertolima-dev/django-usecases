import time

from django.db import transaction
from django.db.models import F
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from apps.ecommerce.models import Order, Product

from .serializers import OrderSerializer


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.select_related("user", "product")
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def perform_create(self, serializer):
        product = serializer.validated_data["product"]
        quantity = serializer.validated_data["quantity"]

        product_locked = Product.objects.select_for_update().get(pk=product.pk)

        if product_locked.stock < quantity:
            raise ValidationError("Estoque insuficiente para este pedido.")

        product_locked.stock = F("stock") - quantity

        time.sleep(5)
        product_locked.save()

        serializer.save(user=self.request.user, paid=True)
