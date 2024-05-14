# Generated by Django 5.0.4 on 2024-05-08 21:52

from django.db import migrations, models

def inicializar_datos_ObjetosValiosos(apps, schema_editor):
    Publicacion_ObjetoValioso = apps.get_model('Trueque', 'Publicacion_ObjetoValioso')
    Publicacion_ObjetoValioso.objects.create(
        tipo='Tipo1',
        marca='Marca1',
        descripcion='Descripción 1',
        estado='Vigente',
        dueño=1,
        foto='img/o_1.jpeg'
    )
    Publicacion_ObjetoValioso.objects.create(
        tipo='Tipo2',
        marca='Marca2',
        descripcion='Descripción 2',
        estado='Proceso',
        dueño=2,
        foto='img/o_2.jpeg'
    )
    Publicacion_ObjetoValioso.objects.create(
        tipo='Tipo3',
        marca='Marca3',
        descripcion='Descripción 3',
        estado='Vigente',
        dueño=3,
        foto='img/o_3.jpeg'
    )
    Publicacion_ObjetoValioso.objects.create(
        tipo='Tipo4',
        marca='Marca4',
        descripcion='Descripción 4',
        estado='Finalizado',
        dueño=4,
        foto='img/o_4.jpeg'
    )
    Publicacion_ObjetoValioso.objects.create(
        tipo='Tipo5',
        marca='Marca5',
        descripcion='Descripción 5',
        estado='Proceso',
        dueño=5,
        foto='img/o_5.jpeg'
    )

def inicializar_datos_Embarcaciones(apps, schema_editor):
    Publicacion_Embarcacion = apps.get_model('Trueque', 'Publicacion_Embarcacion')
    Publicacion_Embarcacion.objects.create(
        embarcacion=1,
        descripcion='Descripción de la Embarcación Fantástica 1',
        estado='Vigente'
    )
    Publicacion_Embarcacion.objects.create(
        embarcacion=2,
        descripcion='Descripción de la Embarcación Fantástica 2',
        estado='Proceso'
    )
    Publicacion_Embarcacion.objects.create(
        embarcacion=3,
        descripcion='Descripción de la Embarcación Fantástica 3',
        estado='Finalizado'
    )
    Publicacion_Embarcacion.objects.create(
        embarcacion=4,
        descripcion='Descripción de la Embarcación Fantástica 4',
        estado='Vigente'
    )
    Publicacion_Embarcacion.objects.create(
        embarcacion=5,
        descripcion='Descripción de la Embarcación Fantástica 5',
        estado='Proceso'
    )

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Publicacion_Embarcacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.TextField()),
                ('estado', models.CharField(max_length=50, choices=[('Vigente', 'Vigente'), ('Proceso', 'Proceso'), ('Finalizado', 'Finalizado')])),
                ('embarcacion', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Publicacion_ObjetoValioso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(max_length=100)),
                ('marca', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('estado', models.CharField(max_length=50)),
                ('dueño', models.IntegerField()),
                ('foto', models.ImageField(upload_to='productos_fotos/')),
            ],
        ),
        
        migrations.RunPython(inicializar_datos_ObjetosValiosos),
        migrations.RunPython(inicializar_datos_Embarcaciones),
        
    ]
