from django.contrib.auth.models import User
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name} (Estoque: {self.stock})"


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, db_index=True) # noqa501
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True, related_name="orders") # noqa501
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Pedido de {self.quantity}x {self.product.name}"
