import django_filters

from .models import Episode


class EpisodeFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name='category')
    tags = django_filters.CharFilter(method='filter_by_queryset')

    def filter_by_queryset(self, queryset, name, value):
        if value:
            tag_ids = [int(id) for id in value.split(',')]
            queryset = queryset.filter(tags__id__in=tag_ids)
        return queryset

    class Meta:
        model = Episode
        fields = ['category', 'tags']
