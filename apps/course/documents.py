from django.db.models import Avg
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from apps.course.models import Category, Course, Instructor, Tag


@registry.register_document
class CourseDocument(Document):
    category = fields.ObjectField(properties={
        "id": fields.IntegerField(),
        "name": fields.TextField(),
    })

    instructor = fields.ObjectField(properties={
        "id": fields.IntegerField(),
        "user": fields.TextField(),  # ou mais detalhado se quiser
    })

    tags = fields.NestedField(properties={
        "id": fields.IntegerField(),
        "name": fields.TextField(),
    })

    avg_rating = fields.FloatField()
    paid_count = fields.IntegerField()

    class Index:
        name = "courses"

    class Django:
        model = Course
        fields = [
            'id',
            'title',
            'description',
            'price',
            'is_active',
            'is_free',
            'workload',
            'start_date',
            'created_at'
        ]
        related_models = [Category, Instructor, Tag]

    def prepare_category(self, instance):
        if instance.category:
            return {
                "id": instance.category.id,
                "name": instance.category.name
            }
        return {}

    def prepare_instructor(self, instance):
        if instance.instructor:
            return {
                "id": instance.instructor.id,
                "user": str(instance.instructor.user)  # personalizável # noqa501
            }
        return {}

    def prepare_tags(self, instance):
        return [{"id": tag.id, "name": tag.name} for tag in instance.tags.all()] # noqa501

    def prepare_avg_rating(self, instance):
        return instance.ratings.aggregate(avg=Avg("rating"))["avg"] or 0.0 # noqa501

    def prepare_paid_count(self, instance):
        return instance.payments.filter(status="paid").count() # noqa501

    @classmethod
    def update_or_create_document(cls, course: Course):
        cls().update(course)

    @classmethod
    def delete_document(cls, course: Course):
        cls().delete(course)
