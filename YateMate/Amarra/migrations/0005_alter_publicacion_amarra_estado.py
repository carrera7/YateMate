# Generated by Django 5.0.4 on 2024-06-02 01:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Amarra', '0004_alter_reserva_fecha_ingreso_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publicacion_amarra',
            name='estado',
            field=models.CharField(choices=[('Vigente', 'Vigente'), ('En Proceso', 'En Proceso'), ('Finalizado', 'Finalizado')], default='Vigente', max_length=20),
        ),
    ]
