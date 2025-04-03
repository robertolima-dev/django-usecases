# serializers.py
from rest_framework import serializers

from apps.book.models import Book, Comment


class CommentSerializer(serializers.ModelSerializer):

    book_id = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.all(), write_only=True, source='book'
    )

    class Meta:
        model = Comment
        fields = ["id", "content", "created_at", "book_id"]
