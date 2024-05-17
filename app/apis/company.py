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
from app.serializers import (
    CompaniesSerializer,
    PaymentMethodsCompaniesSerializer,
)

from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    inline_serializer,
)


# listar compañias de una tienda
class CompaniesListCreate(generics.ListCreateAPIView):
    """
    Ruta para listar y crear compañías de una tienda,
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
            queryset = queryset.filter(pk__in=user.company.all())
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
            queryset = queryset.filter(pk=user.companies)
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
    Ruta para asignar y eliminar método de pago a una compañía,
    debe ser administrador (`is_staff` es `True`)
    o tener el permiso:
    - `view_paymentscompany' para GET
    """
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
                'payment_methods': serializers.ListField(default=[{"payment_method": 1, "bank": 1, "email": "f@gmail.com", "identification":  "v28458411", "phone": "+584129950904" }])
            }
        )
    )
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        company_id = kwargs.get('id')
        payment_methods = request.data.get('payment_methods', [])
        method = request.data.get('method')

        # agregar metodo de pago
        if method:
            for index, value in enumerate(payment_methods):
                payment_methods[index]['company'] = company_id

            serializer = PaymentMethodsCompaniesSerializer(data=payment_methods, many=True)
            serializer.is_valid(raise_exception=True)

            serializer.save(company_id=company_id)
            data = serializer.data
            status_code = status.HTTP_201_CREATED
        # eliminar metodo de pago
        else:

            PaymentMethodsCompanies.objects.filter(id__in=payment_methods).delete()
            data = {"message": "metodo de pago eliminado con éxito"}
            status_code = status.HTTP_200_OK
            
            

        return Response(data, status=status_code)


# consultar el dashboar de una compañia
class DashboardGeneric(generics.GenericAPIView):
    """
    Ruta para consultar el dashboar de una compañia,
    debe ser administrador (`is_staff` es `True`)
    o tener el permiso:
    - `view_paymentscompany' para GET
    """
    queryset = Companies.objects.all()
    permission_classes = [
        permissions.IsAdminUser
        |
        (HasModelPermission)
    ]
    model_permissions = {
        'GET': ['app.view_paymentscompany'],
    }

    def get_queryset(self):
        query = self.queryset
        user = self.request.user
        if not user.is_superuser:
            query = query.filter(pk=user.company)
        return query

    @extend_schema(
        tags=["Companies"],
        parameters=[
            OpenApiParameter(
                name="since",
                description='Filtro fecha desde',
                required=True,
                type=str
            ),
            OpenApiParameter(
                name="until",
                description='Filtro fecha hasta',
                required=True,
                type=str
            ),
            OpenApiParameter(
                name="bank",
                description='Filtro por banco',
                required=False,
                type=int
            ),
            OpenApiParameter(
                name="method",
                description='Filtro por metodo de pago',
                required=False,
                type=int
            ),
        ])
    def get(self, request, *args, **kwargs):
        since = request.query_params.get('since')
        until = request.query_params.get('until')
        bank = request.query_params.get('bank')
        payment_method = request.query_params.get('method')
        company = request.user.companies if request.user.companies else None

        data = get_resource('company').statistics(
            since, until, company, bank, payment_method
        )

        return Response(data)
