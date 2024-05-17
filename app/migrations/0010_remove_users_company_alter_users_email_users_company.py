# Generated by Django 5.0.3 on 2024-05-17 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_alter_historicalpaymentscompany_sender_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='company',
        ),
        migrations.AlterField(
            model_name='users',
            name='email',
            field=models.EmailField(help_text='Correo electrónico', max_length=255, unique=True, verbose_name='email'),
        ),
        migrations.AddField(
            model_name='users',
            name='company',
            field=models.ManyToManyField(help_text='Tienda en la que se encuentra el usuario', null=True, related_name='users', to='app.companies'),
        ),
    ]
