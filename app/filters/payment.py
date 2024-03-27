import django_filters
from app.models import PaymentsCompany

class PaymentsCompanyFilter(django_filters.FilterSet):
    since = django_filters.DateFilter(field_name='date__date', lookup_expr='gte')
    until = django_filters.DateFilter(field_name='date__date', lookup_expr='lte')

    class Meta:
        model = PaymentsCompany
        fields = (
            'bank_origin',
            'bank_destiny',
            'method',
            'since',
            'until',
            'status',
            'company',
        )
