import random
import time

from django.db import transaction
from django.db.models import F
from rest_framework.exceptions import ValidationError

from apps.ecommerce.models import Order, Product


class OrderManager:

    @transaction.atomic
    def create_order(self, user, product, quantity):
        product = Product.objects.select_for_update().get(pk=product.pk)

        if product.stock < quantity:
            raise ValidationError("Estoque insuficiente.")

        # tempo de processamento
        time.sleep(random.uniform(3, 7))

        # payment_processing = bool(random.randint(0, 1))
        payment_processing = True

        Order.objects.create(
            user=user,
            product=product,
            quantity=quantity,
            paid=payment_processing
        )

        if payment_processing:
            product.stock = F("stock") - quantity
            product.save()

        else:
            product.save()
            raise ValidationError('Pagamento não aprovado')
