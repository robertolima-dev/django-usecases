from django.contrib import admin

from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("id", "timestamp", "user", "action", "model", "object_id")
    list_filter = ("action", "model", "timestamp")
    search_fields = ("user__username", "model", "object_repr", "object_id")
    readonly_fields = [field.name for field in AuditLog._meta.fields]
    ordering = ("-timestamp",)

    def has_add_permission(self, request):
        return False  # impedir criação manual

    def has_change_permission(self, request, obj=None):
        return False  # impedir edição

    def has_delete_permission(self, request, obj=None):
        return False  # impedir exclusão
