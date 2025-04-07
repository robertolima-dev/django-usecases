from django.contrib import admin

from apps.notifications.models import (Notification, UserNotificationDeleted,
                                       UserNotificationRead)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'obj_code', 'obj_id', 'message', 'created_at')
    search_fields = ('message', 'obj_code')
    list_filter = ('obj_code', 'created_at')
    ordering = ('-created_at',)


@admin.register(UserNotificationRead)
class UserNotificationReadAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'notification', 'created_at')
    search_fields = ('user__email', 'notification__message')
    autocomplete_fields = ('user', 'notification')
    ordering = ('-created_at',)


@admin.register(UserNotificationDeleted)
class UserNotificationDeletedAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'notification', 'created_at')
    search_fields = ('user__email', 'notification__message')
    autocomplete_fields = ('user', 'notification')
    ordering = ('-created_at',)
