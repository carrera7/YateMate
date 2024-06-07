# Ejemplo de migración problemática

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
        # Elimina esta operación si hace referencia a fecha_salida
        # migrations.RemoveField(
        #     model_name='reserva',
        #     name='fecha_salida',
        # ),
    ]
