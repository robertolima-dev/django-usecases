import django_filters
from django.db.models import Avg, Count, Q
from django_filters import BaseInFilter, CharFilter

from apps.course.models import Course


class CharInFilter(BaseInFilter, CharFilter):
    pass


class CourseFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr="icontains")
    description = django_filters.CharFilter(lookup_expr="icontains")
    price_min = django_filters.NumberFilter(field_name="price", lookup_expr="gte")  # noqa: E501
    price_max = django_filters.NumberFilter(field_name="price", lookup_expr="lte")  # noqa: E501
    start_date_from = django_filters.DateFilter(field_name="start_date", lookup_expr="gte")  # noqa: E501
    start_date_to = django_filters.DateFilter(field_name="start_date", lookup_expr="lte")  # noqa: E501
    workload_min = django_filters.NumberFilter(field_name="workload", lookup_expr="gte")  # noqa: E501
    workload_max = django_filters.NumberFilter(field_name="workload", lookup_expr="lte")  # noqa: E501
    # tags = django_filters.ModelMultipleChoiceFilter(field_name="tags__id", to_field_name="id", queryset=Course.tags.rel.model.objects.all())  # noqa: E501
    tag_ids = CharInFilter(field_name="tags__id", lookup_expr="in")
    tag = django_filters.CharFilter(field_name="tags__name", lookup_expr="iexact")  # noqa: E501
    avg_rating_min = django_filters.NumberFilter(method="filter_avg_rating_min")  # noqa: E501
    min_purchases = django_filters.NumberFilter(method="filter_min_purchases")
    only_free = django_filters.BooleanFilter(method="filter_only_free")
    is_featured = django_filters.BooleanFilter()

    class Meta:
        model = Course
        fields = [
            "is_active",
            "is_free",
            "category",
            "instructor",
        ]

    def filter_only_free(self, queryset, name, value):
        if value:
            return queryset.filter(price=0)
        return queryset

    def filter_avg_rating_min(self, queryset, name, value):
        return queryset.annotate(avg_rating=Avg("ratings__rating")).filter(avg_rating__gte=value)  # noqa: E501

    def filter_min_purchases(self, queryset, name, value):
        return queryset.annotate(
            paid_count=Count("payments", filter=Q(payments__status="paid"))
        ).filter(paid_count__gte=value)
