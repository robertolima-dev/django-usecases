from django.contrib import admin
from django.utils.html import format_html

from apps.sheet_manager.models import (  # noqa: E501
    ManagerSheet,
    SheetPureData,
    SheetSanitizedData,
)


@admin.register(ManagerSheet)
class ManagerSheetAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'type_of_data',
        'file_name',
        'has_formatter',
        'has_table_html',
        'file_status',
        'created_at',
        'updated_at'
    ]
    list_filter = [
        'type_of_data',
        'created_at',
        'updated_at',
        'user'
    ]
    search_fields = [
        'user__username',
        'user__email',
        'file__name',
        'type_of_data'
    ]
    readonly_fields = ['created_at', 'updated_at', 'file_status']
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'file', 'type_of_data')
        }),
        ('Data Processing', {
            'fields': ('formatter', 'table_html'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def file_name(self, obj):
        """Nome do arquivo de forma segura"""
        return obj.get_file_name()
    file_name.short_description = "File Name"

    def file_status(self, obj):
        """Status do arquivo (existe/não existe)"""
        if obj.file_exists():
            return format_html('<span style="color: green;">✓ Existe</span>')
        else:
            return format_html('<span style="color: red;">✗ Não encontrado</span>')  # noqa: E501
    file_status.short_description = "File Status"

    def has_formatter(self, obj):
        return bool(obj.formatter)
    has_formatter.boolean = True
    has_formatter.short_description = "Has Formatter"

    def has_table_html(self, obj):
        return bool(obj.table_html)
    has_table_html.boolean = True
    has_table_html.short_description = "Has Table HTML"

    def save_model(self, request, obj, form, change):
        # Garantir que o usuário seja definido se não estiver
        if not obj.user and request.user.is_authenticated:
            obj.user = request.user
        super().save_model(request, obj, form, change)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Adicionar validação personalizada se necessário
        return form


@admin.register(SheetPureData)
class SheetPureDataAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'manager_sheet',
        'type_data',
        'has_sheet_line',
        'sanitized',
        'created_at'
    ]
    list_filter = [
        'type_data',
        'sanitized',
        'created_at',
        'manager_sheet__user'
    ]
    search_fields = [
        'manager_sheet__user__username',
        'type_data'
    ]
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Basic Information', {
            'fields': ('manager_sheet', 'type_data', 'sanitized')
        }),
        ('Data', {
            'fields': ('sheet_line',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def has_sheet_line(self, obj):
        return bool(obj.sheet_line)
    has_sheet_line.boolean = True
    has_sheet_line.short_description = "Has Sheet Line"


@admin.register(SheetSanitizedData)
class SheetSanitizedDataAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'manager_sheet',
        'type_data',
        'has_sheet_line',
        'created_at'
    ]
    list_filter = [
        'type_data',
        'created_at',
        'manager_sheet__user'
    ]
    search_fields = [
        'manager_sheet__user__username',
        'type_data'
    ]
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Basic Information', {
            'fields': ('manager_sheet', 'type_data')
        }),
        ('Data', {
            'fields': ('sheet_line',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def has_sheet_line(self, obj):
        return bool(obj.sheet_line)
    has_sheet_line.boolean = True
    has_sheet_line.short_description = "Has Sheet Line"
