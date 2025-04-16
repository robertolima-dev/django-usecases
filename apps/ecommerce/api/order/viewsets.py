from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from apps.ecommerce.managers.order_manager import OrderManager
from apps.ecommerce.models import Order

from .serializers import OrderSerializer


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.select_related("user", "product")
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        data = serializer.validated_data
        order = OrderManager().create_order(
            user=self.request.user,
            product=data["product"],
            quantity=data["quantity"]
        )
        serializer.instance = order

    # @transaction.atomic
    # def perform_create(self, serializer):
    #     product = serializer.validated_data["product"]
    #     quantity = serializer.validated_data["quantity"]

    #     updated = Product.objects.filter(
    #         pk=product.pk,
    #         stock__gte=quantity
    #     ).update(stock=F("stock") - quantity)

    #     time.sleep(5)

    #     if not updated:
    #         raise ValidationError("Estoque insuficiente.")

    #     serializer.save(user=self.request.user, paid=True)

        # product_locked = Product.objects.select_for_update().get(pk=product.pk) # noqa501

        # if product_locked.stock < quantity:
        #     raise ValidationError("Estoque insuficiente para este pedido.")

        # product_locked.stock = F("stock") - quantity

        # time.sleep(5)
        # product_locked.save()

        # serializer.save(user=self.request.user, paid=True)
