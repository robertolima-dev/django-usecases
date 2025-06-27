from django.contrib import admin

from apps.ecommerce.models import Order, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "stock", "price", "is_active"]
    list_editable = ["stock", "price", "is_active"]
    search_fields = ["name"]
    list_filter = ["is_active"]
    ordering = ["-id"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "product", "quantity", "total_price", "created_at"]  # noqa: E501
    list_filter = ["created_at"]
    search_fields = ["user__username", "product__name"]
    readonly_fields = ["total_price", "created_at"]
    ordering = ["-created_at"]
