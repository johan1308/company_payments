# Generated by Django 5.0.3 on 2024-03-13 04:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_banks_companies_status_paymentmethods_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='historicalpaymentscompany',
            old_name='receiving_bank',
            new_name='bank_destiny',
        ),
        migrations.RenameField(
            model_name='historicalpaymentscompany',
            old_name='sender_bank',
            new_name='bank_origin',
        ),
        migrations.RemoveField(
            model_name='paymentscompany',
            name='receiving_bank',
        ),
        migrations.RemoveField(
            model_name='paymentscompany',
            name='sender_bank',
        ),
        migrations.AddField(
            model_name='paymentscompany',
            name='bank_destiny',
            field=models.ForeignKey(default=11, help_text='Banco', on_delete=django.db.models.deletion.CASCADE, related_name='distiny_payments', to='app.banks'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='paymentscompany',
            name='bank_origin',
            field=models.ForeignKey(default=1, help_text='Banco', on_delete=django.db.models.deletion.CASCADE, related_name='origin_payments', to='app.banks'),
            preserve_default=False,
        ),
    ]
