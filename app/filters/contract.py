import django_filters
from app.models import Contract

class ContractsGsoftFilterBackend(django_filters.FilterSet):
    since = django_filters.DateFilter(field_name='created_at__date', lookup_expr='gte')
    until = django_filters.DateFilter(field_name='created_at__date', lookup_expr='lte')
    signe = django_filters.BooleanFilter(method='filter_signe')

    class Meta:
        model = Contract
        fields = [
            'since',
            'until',
            'client',
            'status',
            'signe',
            'cycle',
            'client_type',
            'retaining_client',
            'installation_order__sector',
            'installation_order__parish',
        ]

    def filter_signe(self, queryset, name, value):
        
        if value:
            queryset = queryset.filter(signe__isnull=False).all()
            print(queryset)
        else:
            queryset = queryset.filter(signe__isnull=True)

        return queryset