import django_filters
from app.models import InstallationOrder

class InstallationOrderFilter(django_filters.FilterSet):
    building = django_filters.CharFilter(field_name='building', lookup_expr='exact')
    building__isnull = django_filters.BooleanFilter(field_name='building', lookup_expr='isnull')
    status = django_filters.BaseInFilter(field_name='status', lookup_expr='in')
    created_by = django_filters.BaseInFilter(field_name='created_by', lookup_expr='in')
    site = django_filters.BaseInFilter(field_name='invoice_installation__department', lookup_expr='in')

    date_field = django_filters.CharFilter(method='filter_date_field')

    class Meta:
        model = InstallationOrder
        fields = (
            'group',
            'vip',
            'state',
            'status',
            'zone',
            'option',
            'building',
            'building__isnull',
            'payment',
            'confirmation',
            'created_by',
            'site',
        )
        
    def filter_date_field(self, queryset, name, value):
        since = self.data.get('since')
        until = self.data.get('until')
        
        if since and until and value:
            date_field = value.lower()
            gte_param = f'{date_field}__date__gte'
            lte_param = f'{date_field}__date__lte'
            queryset = queryset.filter(**{gte_param: since, lte_param: until})
        
        return queryset
