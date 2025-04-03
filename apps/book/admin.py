# admin.py
from django.contrib import admin

from apps.book.models import Book, Comment, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    search_fields = ["name"]


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "author_name", "tag_list"]
    list_filter = ["tags", "author"]
    search_fields = ["title", "author__name"]
    filter_horizontal = ["tags"]

    def author_name(self, obj):
        return obj.author.email
    author_name.short_description = "Author"

    def tag_list(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()])
    tag_list.short_description = "Tags"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["id", "book", "short_content", "created_at"]
    search_fields = ["content", "book__title"]
    list_filter = ["created_at"]

    def short_content(self, obj):
        return obj.content[:50] + ("..." if len(obj.content) > 50 else "")
    short_content.short_description = "Comment"
