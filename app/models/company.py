from django.db import models
from app.models.base import (
    Status,
    Options,
    BaseModel,
)

# compañias
class Companies(models.Model):
    description = models.TextField(
        null=True,
        help_text='Descripción corta del departamento',
    )
    email = models.CharField(
        max_length=60,
        help_text='email de cada departamento'
    )
    name = models.CharField(
        max_length=50,
        help_text='nombre'
    )
    rif = models.CharField(
        max_length=50,
        help_text='nombre'
    )
    start_date_work = models.DateField(
        auto_now=False,
        auto_now_add=False,
        help_text='fecha en la que empezo adquiri el servicio la empresa'
    )
    status = models.ForeignKey(
        Status,
        default=1,
        on_delete=models.CASCADE,
        help_text='Estado de la compañia',
    )


    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = 'companies'
        ordering = ('name',)


# opciones de compañias
class CompaniesOptions(BaseModel):
    updated_by = None
    updated_at = None
    company = models.ForeignKey(
        Companies,
        on_delete=models.CASCADE,
        related_name='company_options',
        help_text='compañia',
    )
    description = models.CharField(
        max_length=300,
        blank=False,
        null=True,
    )
    option = models.ForeignKey(
        Options,
        on_delete=models.CASCADE,
        related_name='option_companies',
        help_text='opcion'
    )

    class Meta:
        db_table = 'companies_options'
        ordering = ('-id',)
