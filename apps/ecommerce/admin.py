# ecommerce/admin.py
from django.contrib import admin

from .models import Order, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "stock")
    search_fields = ("name",)
    list_filter = ("stock",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "product", "quantity", "paid", "created_at")
    list_filter = ("paid", "created_at", "product")
    search_fields = ("user__username", "product__name")
    readonly_fields = ("created_at",)
