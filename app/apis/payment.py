from django.utils.translation import gettext as _
import datetime
from rest_framework import (
    permissions,
    serializers,
    generics,
    status,
)
from rest_framework.response import Response
from app.permissions import HasModelPermission
from app.models import (
    PaymentMethods,
    PaymentsCompany,
    Companies,
    Banks,
)
from django_filters.rest_framework import (
    DjangoFilterBackend,
)
from drf_spectacular.utils import (
    extend_schema,
    inline_serializer,
)
from app.serializers import (
    PaymentsCompanySerializer,
)
from app.filters import (
    PaymentsCompanyFilter,
)
from app.utils import bool_from_str


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

            # obteniendo rif de la compañia
            company_rif = request.data['objeto']['idComercio']

            # obteniendo compañia a la que va el pago 
            try:
                company = Companies.objects.get(rif=company_rif)
            except Companies.DoesNotExist:
                company = Companies.objects.create(
                    email="unknowncompany@gsoft.com",
                    name="unknown company",
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


# listar pagos de una tienda
class PaymentsCompanyList(generics.ListAPIView):
    """
    Ruta para listar pagos de una tienda,
    debe ser administrador (`is_staff` es `True`)
    o tener el permiso:
    - `view_paymentscompany` para GET,
    """
    
    queryset = PaymentsCompany.objects.all()
    serializer_class = PaymentsCompanySerializer
    filter_backends = (
        DjangoFilterBackend,
    )
    filterset_class = PaymentsCompanyFilter
    permission_classes = [
        permissions.IsAdminUser
        |
        (HasModelPermission)
    ]
    model_permissions = {
        'GET': ['app.view_paymentscompany'],
    }

    def get_queryset(self):
        queryset = self.queryset
        user = self.request.user
        if not user.is_superuser:
            queryset = queryset.filter(company=user.company)
        return queryset

    @extend_schema(tags=["Payments"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


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
            queryset = queryset.filter(company=user.company)
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


# listar los metodos de pago+++
class PaymentMethodsGenerics(generics.GenericAPIView):
    """
    Ruta para listar los bancos,
    debe ser administrador (`is_staff` es `True`)
    o tener el permiso:
    - `view_paymentmethods` para GET,
    """

    queryset = PaymentMethods.objects.all()
    permission_classes = [
        permissions.IsAdminUser
        |
        (HasModelPermission)
    ]
    model_permissions = {
        'GET': ['app.view_paymentmethods'],
    }
    
    @extend_schema(tags=["Payments"]) 
    def get(self, request, *args, **kwargs):
        query = self.get_queryset()
        return Response(query.values(
            'id',
            'currency',
            'name',
            'status',
        ))
