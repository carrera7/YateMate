# Generated by Django 5.0.4 on 2024-06-01 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Amarra', '0003_reserva'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserva',
            name='fecha_ingreso',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='reserva',
            name='fecha_salida',
            field=models.DateField(null=True),
        ),
    ]
