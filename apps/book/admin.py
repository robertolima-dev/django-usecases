# admin.py
from django.contrib import admin

from apps.book.models import Book, Comment, Tag


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    fields = ['id', 'book', 'content', ]
    readonly_fields = ['id', 'book', 'content', ]
    ordering = ['-id']

    def has_delete_permission(self, request, obj=None):
        return False


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
    inlines = [CommentInline]

    def author_name(self, obj):
        return obj.author.email
    author_name.short_description = "Author"

    def tag_list(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()])
    tag_list.short_description = "Tags"
