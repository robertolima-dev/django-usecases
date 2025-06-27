from django.contrib import admin

from .models import UserQuota


@admin.register(UserQuota)
class UserQuotaAdmin(admin.ModelAdmin):
    list_display = ("user", "action", "used", "limit", "remaining", "reset_date")  # noqa: E501
    list_filter = ("action", "reset_date")
    search_fields = ("user__email", "user__username")
    ordering = ("user", "action")

    def remaining(self, obj):
        return obj.limit - obj.used
    remaining.short_description = "Restante"
