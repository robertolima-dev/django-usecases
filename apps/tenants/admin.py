from django.contrib import admin

from .models import Project, Tenant


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'domain', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'domain', 'owner__username', 'owner__email')
    filter_horizontal = ('users',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'tenant', 'is_active', 'created_at')
    list_filter = ('tenant', 'is_active')
    search_fields = ('name', 'tenant__name')
    readonly_fields = ('created_at', 'updated_at')
