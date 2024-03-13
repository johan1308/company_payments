import django_filters
from app.models import PaymentsCompany

class PaymentsCompanyFilter(django_filters.FilterSet):

    # date_field = django_filters.CharFilter(method='filter_date_field')

    class Meta:
        model = PaymentsCompany
        fields = (
            'bank_origin',
        )
        
    # def filter_date_field(self, queryset, name, value):
    #     since = self.data.get('since')
    #     until = self.data.get('until')
        
    #     if since and until and value:
    #         date_field = value.lower()
    #         gte_param = f'{date_field}__date__gte'
    #         lte_param = f'{date_field}__date__lte'
    #         queryset = queryset.filter(**{gte_param: since, lte_param: until})
        
    #     return queryset
