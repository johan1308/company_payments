from django.db import models

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

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = 'companies'
        ordering = ('name',)