from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from apps.ecommerce.managers.order_manager import OrderManager
from apps.ecommerce.models import Order

from .serializers import OrderSerializer


@extend_schema(
    tags=["E-commerce"]
)
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
