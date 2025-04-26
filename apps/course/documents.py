from django.db.models import Avg
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
# edge_ngram => automplete # noqa501
from elasticsearch_dsl import analyzer, token_filter

from apps.course.models import Category, Course, Instructor, Tag

# edge_ngram => automplete
autocomplete_analyzer = analyzer(
    'autocomplete',
    tokenizer="standard",
    filter=["lowercase", token_filter("edge_ngram_filter", type="edge_ngram", min_gram=1, max_gram=20)], # noqa501
)
# edge_ngram => automplete
autocomplete_search_analyzer = analyzer(
    'autocomplete_search',
    tokenizer="standard",
    filter=["lowercase"],
)


@registry.register_document
class CourseDocument(Document):

    # edge_ngram => automplete
    title_autocomplete = fields.TextField(
        analyzer=autocomplete_analyzer,
        search_analyzer=autocomplete_search_analyzer,
    )

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

    # edge_ngram => automplete
    def prepare_title_autocomplete(self, instance):
        return instance.title

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

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, Category):
            return Course.objects.filter(category=related_instance)

        if isinstance(related_instance, Instructor):
            return Course.objects.filter(instructor=related_instance)

        if isinstance(related_instance, Tag):
            return Course.objects.filter(tags=related_instance)
