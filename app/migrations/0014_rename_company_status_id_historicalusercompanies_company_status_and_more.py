# Generated by Django 5.0.3 on 2024-05-17 22:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_historicalusercompanies_company_status_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='historicalusercompanies',
            old_name='company_status_id',
            new_name='company_status',
        ),
        migrations.RenameField(
            model_name='usercompanies',
            old_name='company_status_id',
            new_name='company_status',
        ),
    ]
