from django.contrib import admin

from .models import Message, Room


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'room_type', 'user_list', 'created_at')
    search_fields = ('name', 'users__username')
    list_filter = ('created_at',)
    ordering = ('-created_at',)

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
