from django.db import models
from app.models.managers import (
    UserManager,
)
from app.models.company import Companies
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    Permission,
)


class Users(AbstractBaseUser, PermissionsMixin):
    username = None
    name = models.CharField(
        verbose_name='name',
        max_length=255,
        blank=False,
        help_text='Nombre',
    )
    lastname = models.CharField(
        verbose_name='lastname',
        max_length=255,
        null=True,
        blank=False,
        help_text='Apellido',
    )
    identification = models.CharField(
        max_length=15,
        unique=True,
        blank=False,
        verbose_name='identification',
    )
    phone = models.CharField(
        verbose_name='phone',
        max_length=255,
        null=True,
        blank=False,
        help_text='Numero de telefono',
    )
    email = models.EmailField(
        verbose_name='email',
        max_length=255,
        unique=True,
        blank=False,
        help_text='Correo electronico',
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    company = models.ForeignKey(
        Companies,
        on_delete=models.CASCADE,
        related_name='users',
        help_text='Tienda en la que se encuentra el usuario'
    )

    objects = UserManager()


    class Meta:
        verbose_name = 'users'
        verbose_name_plural = 'users'
        db_table = 'users'
        ordering = ('-id',)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'lastname', 'identification']

    def __str__(self):
        return f'{self.name} {self.lastname}'

    @property
    def full_name(self):
        return self.name+" "+self.lastname
    
    @property
    def short_name(self):
        name = self.name.split()[0]
        lastname = self.lastname.split()[0] if self.lastname else ""
        return name+" "+lastname
