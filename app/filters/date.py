import django_filters
from app.models.invoice import InvoicesGsoft, BalancesGsoft
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.timezone import datetime
from django.db.models import Q

class CreatedAtFilterBackend(DjangoFilterBackend):
    def filter_queryset(self, request, queryset, view):
        created_at_after = request.query_params.get('created_at_after', None)
        created_at_before = request.query_params.get('created_at_before', None)
        if start_date and end_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            queryset = queryset.filter(Q(created_at__gte=created_at_after) & Q(created_at__lte=created_at_before))
        return queryset



class InvoicesDateFilter(django_filters.FilterSet):
    created_at = django_filters.DateFromToRangeFilter(field_name='created_at')
    date_emission_tfhk = django_filters.DateFromToRangeFilter(field_name='date_emission_tfhk')
    date_payment = django_filters.DateFromToRangeFilter(field_name='date_payment')

    class Meta:
        model = InvoicesGsoft
        fields = ['created_at', 'date_emission_tfhk','date_payment']


class BalancesDateFilter(django_filters.FilterSet):
    created_at = django_filters.DateFromToRangeFilter(field_name='created_at')
    updated_at = django_filters.DateFromToRangeFilter(field_name='updated_at')


    class Meta:
        model = BalancesGsoft
        fields = ['created_at', 'updated_at']


class PaymentsDateFilter(django_filters.FilterSet):
    created_at = django_filters.DateFromToRangeFilter(field_name='created_at')
    updated_at = django_filters.DateFromToRangeFilter(field_name='updated_at')


    class Meta:
        model = BalancesGsoft
        fields = ['created_at', 'updated_at']