from django.contrib import admin

from .models import Message, Room


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'user1', 'user2', 'created_at')
    search_fields = ('user1__username', 'user2__username')
    list_filter = ('created_at',)
    ordering = ('-created_at',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'room', 'sender', 'content_preview', 'timestamp', 'is_read') # noqa501
    search_fields = ('sender__username', 'room__user1__username', 'room__user2__username', 'content') # noqa501
    list_filter = ('timestamp', 'is_read')
    ordering = ('-timestamp',)

    def content_preview(self, obj):
        return (obj.content[:40] + '...') if len(obj.content) > 40 else obj.content # noqa501

    content_preview.short_description = 'Mensagem'
