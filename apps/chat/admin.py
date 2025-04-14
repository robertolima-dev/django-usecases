from django.contrib import admin, messages

from common.decorators.admin import admin_action_log

from .models import Message, Room
from .tasks import process_room


@admin_action_log("Disparo processamento assíncrono das salas com sucesso!")
@admin.action(description="Disparar processamento assíncrono das salas")
def trigger_async_process(modeladmin, request, queryset):
    task_count = 0
    for room in queryset:
        process_room.delay(room.id)
        task_count += 1

    if task_count > 0:
        messages.success(request, f"{task_count} tarefas foram enviadas para o Celery!") # noqa501
    else:
        messages.warning(request, "Nenhuma tarefa foi enviada para o Celery.") # noqa501


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    fields = ['id', 'sender', 'type_message', 'content', 'timestamp']
    readonly_fields = ['id', 'sender', 'type_message', 'content', 'timestamp']
    ordering = ['-timestamp']

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'room_type', 'user_list', 'created_at')
    search_fields = ('name', 'users__username')
    list_filter = ('created_at',)
    ordering = ('-created_at',)
    inlines = [MessageInline]
    actions = [trigger_async_process]

    def user_list(self, obj):
        return ", ".join(user.username for user in obj.users.all())
    user_list.short_description = "Participantes"

    def room_type(self, obj):
        return "Privado" if obj.users.count() == 2 else "Grupo"
    room_type.short_description = "Tipo"


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'room', 'sender', 'type_message', 'short_content', 'timestamp', 'is_read') # noqa501
    search_fields = ('sender__username', 'room__name', 'content')
    list_filter = ('type_message', 'timestamp', 'is_read')
    ordering = ('-timestamp',)

    def short_content(self, obj):
        content = obj.content
        if isinstance(content, dict):
            return str(content)[:50]
        return content if len(content) <= 50 else content[:47] + '...'
    short_content.short_description = "Conteúdo"
