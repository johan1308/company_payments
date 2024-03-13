from rest_framework.filters import BaseFilterBackend
from django.db.models import Q


class SinceDateStartFilter(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        since = request.query_params.get('since', request.query_params.get('since_start'))
        if since:
            since += ' 00:00:00.000001'
            queryset = queryset.filter(
                Q(start__gte=since)
            )
        return queryset

    def get_schema_operation_parameters(self, view):
        return [
            {
                'name': 'since',
                'required': False,
                'in': 'query',
                'description': 'Filtrado por fecha `desde` en el campo `start`',
                'schema': {
                    'type': str,
                },
            },
        ]


class UntilDateStartFilter(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        until = request.query_params.get('until_start')
        if until:
            until += ' 23:59:59.000000'
            queryset = queryset.filter(
                Q(start__lte=until)
            )
        return queryset

    def get_schema_operation_parameters(self, view):
        return [
            {
                'name': 'until',
                'required': False,
                'in': 'query',
                'description': 'Filtrado por fecha `hasta` en el campo `start`',
                'schema': {
                    'type': str,
                },
            },
        ]


class SinceDateEndFilter(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        since = request.query_params.get('since', request.query_params.get('since_end'))
        # print(since)
        if since:
            since += ' 00:00:00.000001'
            queryset = queryset.filter(
                Q(end__gte=since)
            )
        return queryset

    def get_schema_operation_parameters(self, view):
        return [
            {
                'name': 'since',
                'required': False,
                'in': 'query',
                'description': 'Filtrado por fecha `desde` en el campo `end`',
                'schema': {
                    'type': str,
                },
            },
        ]


class UntilDateEndFilter(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        until = request.query_params.get('until', request.query_params.get('until_end'))
        print(until)
        if until:
            until += ' 23:59:59.000000'
            queryset = queryset.filter(
                Q(end__lte=until)
            )
            print(queryset)
        return queryset

    def get_schema_operation_parameters(self, view):
        return [
            {
                'name': 'until',
                'required': False,
                'in': 'query',
                'description': 'Filtrado por fecha `hasta` en el campo `end`',
                'schema': {
                    'type': str,
                },
            },
        ]


class SinceCreatedFilter(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        since = request.query_params.get('since', request.query_params.get('since_created_at'))
        # print(since)
        if since:
            since += ' 00:00:00.000001'
            queryset = queryset.filter(
                Q(created_at__gte=since)
            )
        return queryset

    def get_schema_operation_parameters(self, view):
        return [
            {
                'name': 'since',
                'required': False,
                'in': 'query',
                'description': 'Filtrado por fecha `desde` en el campo `created_at`',
                'schema': {
                    'type': str,
                },
            },
        ]


class UntilCreatedFilter(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        until = request.query_params.get('until', request.query_params.get('until_created_at'))
        if until:
            until += ' 23:59:59.000000'
            queryset = queryset.filter(
                Q(created_at__lte=until)
            )
            print(queryset)
        return queryset

    def get_schema_operation_parameters(self, view):
        return [
            {
                'name': 'until',
                'required': False,
                'in': 'query',
                'description': 'Filtrado por fecha `hasta` en el campo `created_at`',
                'schema': {
                    'type': str,
                },
            },
        ]


class StatusCalendarFinishFilter(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        finish = request.query_params.get('finish', None)
        print(finish)
        if finish == "true":
            queryset = queryset.filter(
                Q(finish=True)
            )
        elif finish == "false":
            print(2323)
            queryset = queryset.filter(
                Q(finish__isnull=True)
            )
        return queryset

    def get_schema_operation_parameters(self, view):
        return [
            {
                'name': 'until',
                'required': False,
                'in': 'query',
                'description': 'Filtrado por fecha `hasta` en el campo `created_at`',
                'schema': {
                    'type': str,
                },
            },
        ]


class CalendarUpdatedFilter(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        moved = request.query_params.get('moved', None)
        print(moved)
        if moved == "true":
            print(1)
            queryset = queryset.filter(
                Q(updated_by__isnull=False)
            )
        if moved == "false":
            print(2)
            queryset = queryset.filter(
                Q(updated_by__isnull=True)
            )
        return queryset

    def get_schema_operation_parameters(self, view):
        return [
            {
                'name': 'until',
                'required': False,
                'in': 'query',
                'description': 'Filtrado por fecha `hasta` en el campo `created_at`',
                'schema': {
                    'type': str,
                },
            },
        ]
