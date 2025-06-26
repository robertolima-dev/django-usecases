from django.contrib import admin

from .models import HttpCallLog


@admin.register(HttpCallLog)
class HttpCallLogAdmin(admin.ModelAdmin):
    list_display = ("url", "method", "request_type", "response_time", "created_at")  # noqa: E501
    list_filter = ("method", "status_code", 'request_type', "created_at")
    search_fields = ("url", "response_body", "error_message")
    readonly_fields = (
        "url",
        "method",
        "status_code",
        "request_type",
        "response_time",
        "response_body",
        "error_message",
        "created_at",
    )

    def has_add_permission(self, request):
        return False  # Evita inserções manuais

    def has_change_permission(self, request, obj=None):
        return False  # Registros somente leitura
