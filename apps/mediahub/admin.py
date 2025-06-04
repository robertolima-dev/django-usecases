from django.contrib import admin

from .models import MediaFile


@admin.register(MediaFile)
class MediaFileAdmin(admin.ModelAdmin):
    list_display = ["name", "file", "uploaded_at"]
    search_fields = ["name"]
    readonly_fields = ["uploaded_at"]
