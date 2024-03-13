from django.db import models
from simple_history.models import HistoricalRecords
from app.models.user import Users


class Status(models.Model):
    name = models.CharField(
        max_length=50,
    )
    description = models.CharField(
        max_length=200,
        null=True,
    )
    type = models.IntegerField()

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Statu'
        verbose_name_plural = 'Status'
        db_table = 'status'
        ordering = ('-id',)


class BaseModel(models.Model):
    """
    Base Model
    """
    id = models.BigAutoField(
        primary_key=True,
        editable=False,
        help_text='ID único para la instancia del modelo.'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        null=True,
        help_text='Fecha de creación del objeto',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        null=True,
        help_text='Fecha de actualización del objeto'
    )
    created_by = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        related_name='+',
        null=True
    )
    updated_by = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        related_name='+',
        null=True
    )
    historical = HistoricalRecords(user_model="app.Users", inherit=True)

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value
    class Meta:
        abstract = True