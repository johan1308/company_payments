# Generated by Django 5.0.3 on 2024-04-05 04:01

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_options_alter_historicalpaymentmethods_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalpaymentmethodscompanies',
            name='bank',
            field=models.ForeignKey(blank=True, db_constraint=False, help_text='Banco', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='app.banks'),
        ),
        migrations.AddField(
            model_name='historicalpaymentmethodscompanies',
            name='email',
            field=models.EmailField(help_text='Correo electronico', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='historicalpaymentmethodscompanies',
            name='identification',
            field=models.CharField(help_text='Cedula/rif', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='historicalpaymentmethodscompanies',
            name='phone',
            field=models.CharField(help_text='Telefono', max_length=32, null=True, validators=[django.core.validators.RegexValidator(message='Phone must be in the format +XXXXXXXXXX', regex='^\\+(?:[0-9]){6,32}[0-9]$')]),
        ),
        migrations.AddField(
            model_name='paymentmethodscompanies',
            name='bank',
            field=models.ForeignKey(default=1, help_text='Banco', on_delete=django.db.models.deletion.CASCADE, related_name='payment_methods_companies', to='app.banks'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='paymentmethodscompanies',
            name='email',
            field=models.EmailField(help_text='Correo electronico', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='paymentmethodscompanies',
            name='identification',
            field=models.CharField(help_text='Cedula/rif', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='paymentmethodscompanies',
            name='phone',
            field=models.CharField(help_text='Telefono', max_length=32, null=True, validators=[django.core.validators.RegexValidator(message='Phone must be in the format +XXXXXXXXXX', regex='^\\+(?:[0-9]){6,32}[0-9]$')]),
        ),
        migrations.AlterUniqueTogether(
            name='paymentmethodscompanies',
            unique_together={('company', 'payment_method', 'bank', 'email', 'identification', 'phone')},
        ),
    ]