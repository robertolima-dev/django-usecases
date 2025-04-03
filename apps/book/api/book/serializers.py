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

    class Meta:
        model = Book
        fields = ["id", "title", "author", "tags", "tag_ids", ] # noqa501

    def create(self, validated_data):
        tags = validated_data.pop("tags", [])
        book = Book.objects.create(**validated_data)
        book.tags.set(tags)
        return book

    def update(self, instance, validated_data):
        tags = validated_data.pop("tags", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if tags is not None:
            instance.tags.set(tags)
        return instance
