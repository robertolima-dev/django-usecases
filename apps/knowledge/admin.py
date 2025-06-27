from django.contrib import admin
from django.utils.html import format_html

from .models import KnowledgeStudy, KnowledgeTopic


class KnowledgeStudyInline(admin.TabularInline):
    model = KnowledgeStudy
    extra = 0
    readonly_fields = ("studied_at",)


@admin.register(KnowledgeTopic)
class KnowledgeTopicAdmin(admin.ModelAdmin):
    list_display = ("title", "colored_level", "is_recommended")
    list_filter = ("level", "is_recommended")
    search_fields = ("title", "description")
    list_editable = ("is_recommended",)
    ordering = ("level", "title")
    list_per_page = 25
    actions = ["mark_as_recommended", "mark_as_not_recommended"]
    inlines = [KnowledgeStudyInline]

    @admin.action(description="✅ Marcar como recomendado")
    def mark_as_recommended(self, request, queryset):
        updated = queryset.update(is_recommended=True)
        self.message_user(request, f"{updated} tópico(s) marcados como recomendados.")  # noqa: E501

    @admin.action(description="🚫 Marcar como não recomendado")
    def mark_as_not_recommended(self, request, queryset):
        updated = queryset.update(is_recommended=False)
        self.message_user(request, f"{updated} tópico(s) marcados como não recomendados.")  # noqa: E501

    def colored_level(self, obj):
        color = {
            "fundamental": "#0277bd",
            "intermediate": "#f9a825",
            "advanced": "#c62828",
        }.get(obj.level, "#9e9e9e")

        label = obj.get_level_display().upper()
        return format_html(
            f"<span style='background:{color}; color:#fff; padding:4px 8px; border-radius:4px;'>{label}</span>"  # noqa: E501
        )

    colored_level.short_description = "Nível"
    colored_level.admin_order_field = "level"
