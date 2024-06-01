# Generated by Django 5.0.4 on 2024-05-30 21:52

import datetime
from django.db import migrations, models
import django.db.models.deletion

def create_initial_amarras(apps, schema_editor):
    Publicacion_Amarra = apps.get_model('Amarra', 'Publicacion_Amarra')
    User = apps.get_model('Register', 'User')

    # Obtener instancias de usuario
    user1 = User.objects.first()
    user2 = User.objects.last()

    if user1 and user2:
        Publicacion_Amarra.objects.create(
            dueño=user1,
            precio="100.00",
            fecha_inicio=datetime.date(2024, 6, 1),
            cant_dias="10",
            ubicacion='Ubicación 1'
        )
        Publicacion_Amarra.objects.create(
            dueño=user2,
            precio="200.00",
            fecha_inicio=datetime.date(2024, 6, 15),
            cant_dias="20",
            ubicacion='Ubicación 2'
        )

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Register', '0005_alter_embarcacion_foto'),
    ]

    operations = [
        migrations.CreateModel(
            name='Publicacion_Amarra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('precio', models.TextField()),
                ('fecha_inicio', models.DateField()),
                ('cant_dias', models.TextField()),
                ('ubicacion', models.TextField()),
                ('dueño', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Register.user')),
            ],
        ),
        migrations.RunPython(create_initial_amarras),
    ]
