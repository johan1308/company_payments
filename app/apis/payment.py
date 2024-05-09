from django.utils.translation import gettext as _
import datetime
from django.db.models import Q
from rest_framework import (
    permissions,
    serializers,
    generics,
    filters,
    status,
)
from rest_framework.response import Response
from app.permissions import HasModelPermission
from app.models import (
    Banks,
    Companies,
    PaymentMethods,
    PaymentsCompany,
    PaymentMethodsCompanies,
)
from django_filters.rest_framework import (
    DjangoFilterBackend,
)
from drf_spectacular.utils import (
    extend_schema,
    inline_serializer,
)
from app.serializers import (
    PaymentMethodsSerializer,
    PaymentsCompanySerializer,
)
from app.filters import (
    PaymentsCompanyFilter,
)

# registrar pagos a la compañia desde los bancos
class PaymentCompanyBanksGeneric(generics.GenericAPIView):
    """
    Ruta para registrar pagos a la compañia desde los banco,
    debe ser administrador (`is_staff` es `True`)
    o tener el permiso:
    - `add_paymentscompany` para POST,
    """
    permission_classes = [
        permissions.IsAdminUser
        |
        (HasModelPermission)
    ]
    model_permissions = {
        'POST': ['app.add_paymentscompany'],
    }

    @extend_schema(
        tags=["Payments"],
        request=inline_serializer(
        name='PaymentDebtTDC',
        fields={
            'codigo': serializers.CharField(required=True),
            'fecha': serializers.CharField(required=True),
            'hora': serializers.CharField(required=True),
            'monto': serializers.CharField(required=True),
        })
    )
    def post(self, request, *args, **kwargs):
        fields = ['objeto', 'fecha', 'hora', 'codigoMoneda', 'monto', 'tipo']
        object_fields =  ['referenciaBancoOrigen', 'idComercio', 'concepto', 'BancoOrigen', 'BancoDestino', 'numCliente']
        
        for field in fields:
            for object_field in object_fields:
                if object_field not in request.data['objeto']:
                    return Response({f"objeto.{object_field}": "this field is required"}, status=status.HTTP_400_BAD_REQUEST)

            if field not in request.data:
                return Response({field: "this field is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # formateando fecha y hora
            date_str = request.data['fecha']
            hour_str = request.data["hora"]

            date = datetime.datetime.strptime(date_str, "%Y%m%d")
            hour = datetime.datetime.strptime(hour_str, "%H%M")

            combined_datetime = date.replace(hour=hour.hour, minute=hour.minute, second=0)

            # obteniendo referencia
            reference = request.data['objeto']['referenciaBancoOrigen']

            if len(reference) > 6:
                pass

            # obteniendo rif de la compañia
            company_rif = request.data['objeto']['idComercio']

            # obteniendo compañia a la que va el pago 
            try:
                company = Companies.objects.get(rif=company_rif)
            except Companies.DoesNotExist:
                company = Companies.objects.create(
                    email="unknowncompany@gsoft.com",
                    name="unknown company",
                    rif=company_rif,
                    start_date_work=datetime.date.today(),   
                )

            # obteniendo descripcion del pago
            description = request.data['objeto']['concepto']
            bank_code_origin = request.data['objeto']['BancoOrigen']
            bank_code_destiny = request.data['objeto']['BancoDestino']

            # instanciando banco origen 
            try:
                bank_origin = Banks.objects.get(code=bank_code_origin)
            except Banks.DoesNotExist:
                bank_origin = Banks.objects.create(
                    name=bank_code_origin,
                    code=bank_code_origin,
                )

            # instanciando banco destino
            try:
                bank_destiny = Banks.objects.get(code=bank_code_destiny)
            except Banks.DoesNotExist():
                bank_destiny = Banks.objects.create(
                    name=bank_destiny,
                    code=bank_destiny,
                )

            # obteniendo numero de tlf
            phone = request.data['objeto']['numCliente']
            phone = phone[-11:] if phone is not None else None

            if phone and phone[0] == '8':
                phone = f'0{phone[-10:]}'

            if PaymentsCompany.objects.filter(
                reference=reference,
                mobile=phone,
                company=company,
            ).exists():
                return Response({"message": "Payment is registered", "field": None}, status.HTTP_400_BAD_REQUEST)

            PaymentsCompany.objects.create(
                method_id=1 if request.data['tipo'] in ['P2C', 'P2P'] else 2,
                bank_origin=bank_origin,
                bank_destiny=bank_destiny,
                amount=request.data['monto'],
                date=combined_datetime,
                description=description,
                mobile=phone,
                reference=reference,
                created_by=request.user,
                company=company
            )

        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"message": "Payment successfully registered"}, status=status.HTTP_201_CREATED)


# validar pagos
class PaymentsCompanyGeneric(generics.GenericAPIView):
    """
    Ruta para validar pagos,
    debe ser administrador (`is_staff` es `True`)
    o tener el permiso:
    - `validate_paymentscompany` para POST,
    """
    serializer_class = PaymentsCompanySerializer

    @extend_schema(
        tags=["Payments"],
        request=inline_serializer(
            name='PaymentsCompanyGeneric',
            fields={
                'amount': serializers.DecimalField(max_digits=50, decimal_places=2),
                'reference': serializers.CharField(required=True),
                'mobile': serializers.CharField(required=True),
                'sender': serializers.CharField(required=True),
                'method': serializers.IntegerField(required=True),
                'date': serializers.DateField(required=True),
            }
        ))
    def post(self, request, *args, **kwargs):
        fields = ['amount', 'reference', 'mobile', 'sender', 'method', 'date']

        for field in fields:
            if field not in request.data:
                return Response({field: "this field is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            amount = request.data.get('amount')
            reference = request.data.get('reference')
            sender = request.data.get('sender')
            mobile = request.data.get('mobile')
            method = request.data.get('method')
            date = request.data.get('date')

            date = datetime.datetime.strptime(date, '%Y-%m-%d').date()

            user = request.user

            
            if len(reference) != 6:
                return Response({"message": "Error, campo 'reference' solo debe tener 6 digitos"})


            query = PaymentsCompany.objects.filter(
                # date__date=date, #TODO REVISAR
                amount=str(amount),
                reference__endswith=reference,
                method_id=method,
                sender=sender,
                status=True,
                company=user.company,
            )

            if method == 1:
                query = query.filter(mobile=mobile)

            if not query:
                return Response(
                    {'message': _('Pago no encontrado')},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if query.count() > 1:
                return Response(
                    {"message": f"{query.count()} pagos encontrados"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        except Exception as e:
            return Response({"message": e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        instance = query.first()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


# listar y crear pagos de una empresa
class PaymentsCompanyListCreate(generics.ListCreateAPIView):
    """
    Ruta para listar y crear pagos de una empresa,
    debe ser administrador (`is_staff` es `True`)
    o tener el permiso:
    - `view_paymentscompany` para GET,
    - `add_paymentscompany` para POST,
    """

    queryset = PaymentsCompany.objects.all()
    serializer_class = PaymentsCompanySerializer
    filter_backends = (
        filters.SearchFilter,
        DjangoFilterBackend,
    )
    filterset_class = PaymentsCompanyFilter
    search_fields = (
        'sender',
        'reference',
        'mobile',
    )
    permission_classes = [
        permissions.IsAdminUser
        |
        (HasModelPermission)
    ]
    model_permissions = {
        'GET': ['app.view_paymentscompany'],
        'POST': ['app.add_paymentscompany'],
    }

    def get_queryset(self):
        queryset = self.queryset
        user = self.request.user
        if not user.is_superuser:
            payment_methods_company = PaymentMethodsCompanies.objects.filter(
                company=user.company,
                status_id=1,
                payment_method__status_id=1
            ).only('payment_method')

            queryset = queryset.filter(company=user.company, method__in=payment_methods_company.values('payment_method'))
        return queryset

    @extend_schema(tags=["Payments"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        user = request.user

        # si no es superuser se asocia la compa;ia del usuario que hace la peticion 
        if not user.is_superuser:
            request.data['company'] = request.user.company.pk

        request.data['created_by'] = request.user.pk
        return super().post(request, *args, **kwargs)



# ver y validar pago de una empresa
class PaymentsCompanyRetrieveUpdate(generics.RetrieveUpdateAPIView):
    """
    Ruta para ver y validar pago de una empresa,
    debe ser administrador (`is_staff` es `True`)
    o tener el permiso:
    - `view_paymentscompany` para GET,
    - `change_paymentscompany` para PATCH,
    """

    lookup_url_kwarg = 'id'
    lookup_field = 'id'
    queryset = PaymentsCompany.objects.all()
    serializer_class = PaymentsCompanySerializer
    permission_classes = [
        permissions.IsAdminUser
        |
        (HasModelPermission)
    ]
    model_permissions = {
        'GET': ['app.view_paymentscompany'],
        'PATCH': ['app.change_paymentscompany'],
    }

    def get_queryset(self):
        queryset = self.queryset
        user = self.request.user
        if not user.is_superuser:
            payment_methods_company = PaymentMethodsCompanies.objects.filter(
                company=user.company,
                status_id=1,
                payment_method__status_id=1
            ).only('payment_method')

            queryset = queryset.filter(company=user.company, method__in=payment_methods_company.values('payment_method'))
        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['retrieve'] = True
        return context

    @extend_schema(tags=["Payments"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(exclude=True)
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
    
    @extend_schema(
        tags=["Payments"],
        request=inline_serializer(
        name='PaymentsCompanyRetrieveUpdate',
        fields={
            'status': serializers.BooleanField(required=True)
        })
    )
    def patch(self, request, *args, **kwargs):
        for key, value in request.data.items():
            if key != 'status':
                return Response(
                    {"message": "Error, solo disponible campo 'status'"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        status_data = request.data.get('status')

        if status_data:
            return Response({"message": "Error, el pago solo se puede inactivar"}, status=status.HTTP_400_BAD_REQUEST)

        request.data['updated_by'] = request.user.pk
        return super().patch(request, *args, **kwargs)


# listar los bancos
class BanksGeneric(generics.GenericAPIView):
    """
    Ruta para listar los bancos,
    debe ser administrador (`is_staff` es `True`)
    o tener el permiso:
    - `view_banks` para GET,
    """

    queryset = Banks.objects.all()
    permission_classes = [
        permissions.IsAdminUser
        |
        (HasModelPermission)
    ]
    model_permissions = {
        'GET': ['app.view_banks'],
    }
    
    @extend_schema(tags=["Payments"]) 
    def get(self, request, *args, **kwargs):
        query = self.get_queryset()
        return Response(query.values(
            'id',
            'achronym',
            'code',
            'name',
        ))


# listar y registrar metodos de pagos
class PaymentMethodsGenerics(generics.ListCreateAPIView):
    """
    Ruta para listar y registrar metodos de pagos,
    debe ser administrador (`is_staff` es `True`)
    o tener el permiso:
    - `view_paymentmethods` para GET,
    """

    queryset = PaymentMethods.objects.all()
    serializer_class = PaymentMethodsSerializer
    permission_classes = [
        permissions.IsAdminUser
        |
        (HasModelPermission)
    ]
    model_permissions = {
        'GET': ['app.view_paymentmethods'],
        'POST': ['app.add_paymentmethods'],
    }


    def get_queryset(self):
        user = self.request.user
        if not user.is_superuser and user.company:
            payment_methods = PaymentMethodsCompanies.objects.filter(company=user.company).values('payment_method')
            return self.queryset.filter(id__in=payment_methods)
        return self.queryset


    @extend_schema(tags=["Payments"]) 
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


    @extend_schema(tags=["Payments"])
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer_class(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
