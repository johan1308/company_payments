import datetime
from rest_framework import (
    permissions,
    serializers,
    generics,
    status,
)
from rest_framework.response import Response
from app.permissions import HasModelPermission
from app.models import PaymentsCompany, Banks, Companies
from django_filters.rest_framework import (
    DjangoFilterBackend,
)
from drf_spectacular.utils import (
    extend_schema,
    inline_serializer,
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
    queryset = PaymentsCompany.objects.all()
    filter_backends = (
        DjangoFilterBackend,
    )
    filterset_class = PaymentsCompanyFilter

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
                return Response({"message": f"There is no user with the rif: {company_rif}", "field": "idComercio"}, status=status.HTTP_400_BAD_REQUEST)

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


    def get_queryset(self):
        query = super().get_queryset()
        return query

    # def get(self, request, *args, **kwargs):

    #     return self.get_queryset.values()