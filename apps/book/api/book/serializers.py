from rest_framework import serializers

from apps.book.models import Book, Tag
from apps.users.api.auth.serializers import UserSimpleSerializer


class TagNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]


class BookSerializer(serializers.ModelSerializer):
    author = UserSimpleSerializer(read_only=True)
    tags = TagNestedSerializer(read_only=True, many=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all(), write_only=True, source='tags'
    )
    comments_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Book
        fields = ["id", "title", "author", "tags", "tag_ids", "comments_count"]
