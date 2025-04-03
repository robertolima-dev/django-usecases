# course/filters.py
import django_filters

from apps.course.models import Course


class CourseFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr="icontains")
    description = django_filters.CharFilter(lookup_expr="icontains")
    price_min = django_filters.NumberFilter(field_name="price", lookup_expr="gte") # noqa501
    price_max = django_filters.NumberFilter(field_name="price", lookup_expr="lte") # noqa501
    start_date_from = django_filters.DateFilter(field_name="start_date", lookup_expr="gte") # noqa501
    start_date_to = django_filters.DateFilter(field_name="start_date", lookup_expr="lte") # noqa501
    workload_min = django_filters.NumberFilter(field_name="workload", lookup_expr="gte") # noqa501
    workload_max = django_filters.NumberFilter(field_name="workload", lookup_expr="lte") # noqa501
    tags = django_filters.ModelMultipleChoiceFilter(field_name="tags__id", to_field_name="id", queryset=Course.tags.rel.model.objects.all()) # noqa501

    class Meta:
        model = Course
        fields = [
            "is_active",
            "is_free",
            "category",
            "instructor",
        ]
