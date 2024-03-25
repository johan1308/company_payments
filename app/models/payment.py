from django.utils.translation import gettext as _
from django.db import models
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
        on_delete=models.CASCADE,
        help_text='Estado de Factura'
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Payment Form'
        verbose_name_plural = 'Payment Forms'
        db_table = 'payment_methods'
        ordering = ('-id',)


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
        help_text='nombre de la cuenta del zelle'
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
