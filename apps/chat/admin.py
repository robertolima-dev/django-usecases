from django.contrib import admin

from .models import Message, Room


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "room", "user", "content", "timestamp")
    list_filter = ("room", "user")
    search_fields = ("content",)
    ordering = ("-timestamp",)
