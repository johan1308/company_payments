from django.utils.translation import gettext as _
from django.db import models
from django.core.validators import RegexValidator
from app.models.base import (
    Status,
    BaseModel,
)
from app.models.company import Companies


class Banks(models.Model):
    achronym = models.CharField(
        max_length=10,
        null=True,
        unique=True,
        help_text='Acronimo del banco'
    )
    code = models.CharField(
        max_length=10,
        null=False,
        unique=True,
        db_column='code',
        help_text='Codigo del banco'
    )
    name = models.CharField(
        max_length=100,
        help_text='Nombre del banco'
    )


    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Bank'
        verbose_name_plural = 'Banks'
        db_table = 'banks'
        ordering = ('-id',)
        

class PaymentMethods(BaseModel):
    currency = models.CharField(
        max_length=100,
        help_text='Divisa/Moneda de la forma de pago'
    )
    name = models.CharField(
        max_length=100,
        help_text='Forma de pago'
    )
    status = models.ForeignKey(
        Status,
        default=1,
        on_delete=models.CASCADE,
        help_text='Estado del metodo de pago'
    )

    
    class Meta:
        db_table = 'payment_methods'
        ordering = ('-id',)


class PaymentMethodsCompanies(BaseModel):
    updated_by = None
    updated_at = None
    company = models.ForeignKey(
        Companies,
        on_delete=models.CASCADE,
        related_name='payment_methods_companies',
        help_text='compañia',
    )
    payment_method = models.ForeignKey(
        PaymentMethods,
        on_delete=models.CASCADE,
        related_name='companies_payment_methods',
        help_text='metodo de pago'
    )
    bank = models.ForeignKey(
        Banks,
        on_delete=models.CASCADE,
        help_text='Banco',
        related_name='payment_methods_companies',
    )
    status = models.ForeignKey(
        Status,
        default=1,
        on_delete=models.CASCADE,
        help_text='status del metodo de pago de la compalia'
    )
    email = models.EmailField(
        null=True,
        max_length=255,
        help_text='Correo electronico',
    )
    identification = models.CharField(
        null=True,
        max_length=20,
        help_text='Cedula/rif',
    )
    phone = models.CharField(
        null=True,
        max_length=32,
        help_text='Telefono',
        validators=[
            RegexValidator(
                regex=r'^\+(?:[0-9]){6,32}[0-9]$',
                message=_('Phone must be in the format +XXXXXXXXXX'),
            ),
        ],
    )



    class Meta:
        db_table = 'payment_methods_companies'
        ordering = ('-id',)
        unique_together = ('company', 'payment_method', 'bank', 'email', 'identification', 'phone',)


class PaymentsCompany(BaseModel):
    company = models.ForeignKey(
        Companies,
        on_delete=models.CASCADE,
        help_text='Compañia que esta adquiriendo el servicio',
        related_name='payments_company',
    )
    bank_origin = models.ForeignKey(
        Banks,
        on_delete=models.CASCADE,
        help_text='Banco',
        related_name='origin_payments',
    )
    bank_destiny = models.ForeignKey(
        Banks,
        on_delete=models.CASCADE,
        help_text='Banco',
        related_name='distiny_payments',
    )
    method = models.ForeignKey(
        PaymentMethods,
        on_delete=models.CASCADE,
        help_text='Método de pago',
        related_name='payment_company'
    )
    amount = models.DecimalField(
        max_digits=50,
        decimal_places=2,
        help_text='Monto del pago',
    )
    date = models.DateTimeField(
        auto_now_add=False,
        help_text='Fecha en la que se registro el pago',
    )
    description = models.CharField(
        max_length=300,
        blank=False,
        null=True,
    )
    mobile = models.CharField(
        max_length=300,
        blank=False,
        null=True,
        help_text='Titular enviante de transacción'
    )
    reference = models.TextField(
        blank=False,
        null=True,
        help_text='referencia de pagomovil/transferencia'
    )
    sender = models.CharField(
        max_length=300,
        blank=False,
        null=True,
        help_text='nombre del titular del zelle'
    )
    status = models.BooleanField(default=True)

    def __str__(self) -> str:
        return str(self.pk)

    
    class Meta:
        db_table = 'payments_company'
        ordering = ('-id',)
        permissions = (
            ('validate_paymentscompany', _('Can validate Payments Company')),
        )