# Generated by Django 5.0.3 on 2024-05-17 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_historicalpaymentmethodscompanies_bank_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalpaymentscompany',
            name='sender',
            field=models.CharField(help_text='nombre del titular del zelle', max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='paymentscompany',
            name='sender',
            field=models.CharField(help_text='nombre del titular del zelle', max_length=300, null=True),
        ),
    ]
