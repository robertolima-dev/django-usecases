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
    category = CategorySerializer(read_only=True)
    instructor = InstructorSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source="category", write_only=True
    )
    instructor_id = serializers.PrimaryKeyRelatedField(
        queryset=Instructor.objects.all(), source="instructor", write_only=True
    )
    tag_ids = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True, source="tags", write_only=True
    )

    avg_rating = serializers.FloatField(read_only=True)
    paid_count = serializers.IntegerField(read_only=True)

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

            # combine
            "avg_rating",
            "paid_count",

            # read
            "category", "instructor", "tags",

            # write
            "category_id", "instructor_id", "tag_ids",
        ]
        read_only_fields = ["id", "created_at"]


class CourseSearchSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    price = serializers.DecimalField(max_digits=8, decimal_places=2, read_only=True)  # noqa: E501
    is_active = serializers.BooleanField(read_only=True)
    is_free = serializers.BooleanField(read_only=True)
    workload = serializers.IntegerField(read_only=True)
    start_date = serializers.DateTimeField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    avg_rating = serializers.FloatField(read_only=True)
    paid_count = serializers.IntegerField(read_only=True)

    category = serializers.DictField(read_only=True)  # espera {"id": int, "name": str}  # noqa: E501
    instructor = serializers.DictField(read_only=True)  # espera {"id": int, "user": str}  # noqa: E501
    tags = serializers.ListField(child=serializers.DictField(), read_only=True)  # noqa: E501
