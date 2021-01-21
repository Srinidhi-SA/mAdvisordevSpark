from builtins import object
import django_filters
from api.models import Dataset


class DatasetFilters(django_filters.FilterSet):

    def filter_queryset(self):
        pass

    name = django_filters.CharFilter(lookup_expr='iexact')
    db_type = django_filters.CharFilter(lookup_expr='iexact')
    deleted = django_filters.BooleanFilter()
    bookmarked = django_filters.BooleanFilter()

    class Meta(object):
        model = Dataset
        fields = ['bookmarked', 'deleted', 'db_type', 'name']