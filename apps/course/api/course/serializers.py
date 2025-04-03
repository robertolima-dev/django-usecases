from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.course.models import Category, Course, Instructor, Tag

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]


class InstructorSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Instructor
        fields = ["id", "user", "bio"]


class CourseSerializer(serializers.ModelSerializer):
    # leitura
    category = CategorySerializer(read_only=True)
    instructor = InstructorSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    # escrita
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source="category", write_only=True
    )
    instructor_id = serializers.PrimaryKeyRelatedField(
        queryset=Instructor.objects.all(), source="instructor", write_only=True
    )
    tag_ids = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True, source="tags", write_only=True
    )

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "description",
            "price",
            "is_active",
            "is_free",
            "workload",
            "start_date",
            "created_at",

            # read
            "category", "instructor", "tags",

            # write
            "category_id", "instructor_id", "tag_ids",
        ]
        read_only_fields = ["created_at"]
