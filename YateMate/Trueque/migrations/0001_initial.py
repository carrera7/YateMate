from django.db import migrations, models
from Register.models import User

def inicializar_datos_ObjetosValiosos(apps, schema_editor):
    User = apps.get_model('Register', 'User')  # Importa el modelo User
    Publicacion_ObjetoValioso = apps.get_model('Trueque', 'Publicacion_ObjetoValioso')

    # Obtener instancias de User
    user1 = User.objects.get(pk=1)
    user2 = User.objects.get(pk=2)

    # Crear las instancias de Publicacion_ObjetoValioso con los dueños correctos y matrículas
    Publicacion_ObjetoValioso.objects.create(
        tipo='Tipo1',
        marca='Marca1',
        descripcion='Descripción 1',
        estado='Vigente',
        dueño=user1,  # Asigna la instancia de User
        foto='o_1.jpeg',
        matricula='123ABC'  # Agrega la matrícula
    )
    Publicacion_ObjetoValioso.objects.create(
        tipo='Tipo2',
        marca='Marca2',
        descripcion='Descripción 2',
        estado='Proceso',
        dueño=user2,
        foto='o_2.jpeg',
        matricula='456DEF'  # Agrega la matrícula
    )

def inicializar_datos_Embarcaciones(apps, schema_editor):
    Publicacion_Embarcacion = apps.get_model('Trueque', 'Publicacion_Embarcacion')
    Publicacion_Embarcacion.objects.create(
        embarcacion=1,
        descripcion='Descripción de la Embarcación Fantástica 1',
        estado='Vigente'
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
                ('dueño', models.ForeignKey(null=True, on_delete=models.SET_NULL, to='Register.User')),
                ('foto', models.ImageField(upload_to='img_pu/')),
                ('matricula', models.CharField(max_length=50))  # Agrega el campo matricula
            ],
        ),
        
        migrations.RunPython(inicializar_datos_ObjetosValiosos),
        migrations.RunPython(inicializar_datos_Embarcaciones),
        
    ]
