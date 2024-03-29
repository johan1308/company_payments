from django.utils.translation import gettext as _
from rest_framework import (
    permissions,
    serializers,
    generics,
    filters,
    status,
)
from rest_framework.response import Response
from django_filters.rest_framework import (
    DjangoFilterBackend,
)
from django.db import transaction
from app.resources import get_resource
from app.permissions import HasModelPermission
from app.models import (
    Companies,
    PaymentMethods,
    CompaniesOptions,
    PaymentMethodsCompanies,
    
)
from app.models.base import Options
from app.serializers import CompaniesSerializer
from drf_spectacular.utils import (
    extend_schema,
    inline_serializer,
)


# listar compañias de una tienda
class CompaniesListCreate(generics.ListCreateAPIView):
    """
    Ruta para listar y crear compañias de una tienda,
    debe ser administrador (`is_staff` es `True`)
    o tener el permiso:
    - `view_companies` para GET,
    - `add_companies` para POST,
    """
    
    queryset = Companies.objects.all()
    serializer_class = CompaniesSerializer
    filter_backends = (
        filters.SearchFilter,
        DjangoFilterBackend,
    )
    filterset_fields = (
        'status',
    ) 
    search_fields = (
        'name',
        'email',
        'rif',
    )
    permission_classes = [
        permissions.IsAdminUser
        |
        (HasModelPermission)
    ]
    model_permissions = {
        'GET': ['app.view_companies'],
        'POST': ['app.add_companies'],
    }

    def get_queryset(self):
        queryset = self.queryset
        user = self.request.user
        if not user.is_superuser:
            queryset = queryset.filter(pk=user.company)
        return queryset

    @extend_schema(tags=["Companies"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(tags=["Companies"])
    def post(self, request, *args, **kwargs):
        request.data['created_by'] = request.user.pk
        return super().post(request, *args, **kwargs)


# consultar y cambiar status a una compañia
class CompaniesRetrieveUpdate(generics.RetrieveUpdateAPIView):
    """
    Ruta para consultar y cambiar status a una compañia,
    debe ser administrador (`is_staff` es `True`)
    o tener el permiso:
    - `view_companies` para GET,
    - `change_companies` para PATCH,
    """
    lookup_url_kwarg = 'id'
    lookup_field = 'id'
    queryset = Companies.objects.all()
    serializer_class = CompaniesSerializer
    permission_classes = [
        permissions.IsAdminUser
        |
        (HasModelPermission)
    ]
    model_permissions = {
        'GET': ['app.view_companies'],
        'PATCH': ['app.change_companies'],
    }

    def get_queryset(self):
        queryset = self.queryset
        user = self.request.user
        if not user.is_superuser:
            queryset = queryset.filter(pk=user.company)
        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['retrieve'] = True
        return context

    @extend_schema(tags=["Companies"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(exclude=True)
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        tags=["Companies"],
        request=inline_serializer(
            name='CompaniesRetrieveUpdate',
            fields={
                'status': serializers.IntegerField(default=1),
                'options': serializers.ListField(default=[{"id": 1, "description": True}])
            }
        )
    )
    @transaction.atomic
    def patch(self, request, *args, **kwargs):

        status_company = request.data.get('status')
        options = request.data.pop('options')
        id = kwargs.get('id')

        request.data['updated_by'] = request.user.pk
        data = super().patch(request, *args, **kwargs)

        if status_company is False:
            get_resource('base').assign_record_to_model(
                id,
                Companies,
                CompaniesOptions,
                Options,
                options,
                'company',
                'option',
                True,
                False,
                request.user
            )
        
        return data


# asignar y eliminar metodo de pago a una compañia
class CompaniesPaymentMethodsGeneric(
    generics.GenericAPIView,
):
    """
    Ruta para asignar y eliminar metodo de pago a una compañia,
    debe ser administrador (`is_staff` es `True`)
    o tener el permiso:
    - `view_paymentscompany' para GET
    """
    lookup_field = 'id'
    lookup_url_kwarg = 'id'
    model = PaymentMethodsCompanies
    filter_backends = (
        DjangoFilterBackend,
    )
    permission_classes = [
        permissions.IsAdminUser
        |
        (HasModelPermission)
    ]
    model_permissions = {
        'GET': ['app.view_paymentscompany'],
    }

    @extend_schema(
        tags=["Companies"],
        request=inline_serializer(
            name='CompaniesPaymentMethodsGeneric',
            fields={
                'method': serializers.BooleanField(default=True),
                'payment_methods': serializers.ListField(default=[{"id": 1, "status": 1}])
            }
        )
    )
    def post(self, request, *args, **kwargs):

        company_id = kwargs.get('id')
        payment_methods = request.data.get('payment_methods', [])
        method = request.data.get('method')
        
        message, status_code = get_resource('base').assign_record_to_model(
            company_id,
            Companies,
            self.model,
            PaymentMethods,
            payment_methods,
            'company',
            'payment_method',
            method,
            True,
            request.user
        )

        return Response({"message": _(message)}, status=status_code)
