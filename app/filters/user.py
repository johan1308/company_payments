import django_filters
from app.models import User


class UserMultipleChoiceFilter(django_filters.FilterSet):
    management = django_filters.BaseInFilter(field_name='management', lookup_expr='in')
    
    class Meta:
        model = User
        fields = (
            'management',
        )