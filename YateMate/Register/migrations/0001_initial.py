from django.db import migrations, models
from django.utils import timezone
from datetime import date
from django.core.validators import MinValueValidator, MaxValueValidator

def inicializar_datos_User(apps, schema_editor):
    User = apps.get_model('Register', 'User')  # Reemplaza 'tu_app' con el nombre real de tu aplicación Django
    user_data = [
        {
            'mail': 'usuario1@mail.com',
            'tipo': 'Usuario',  # Aquí debes poner la clave foránea a otro Usuario si es relevante para tu aplicación
            'password': 'password1',
            'nombre': 'Nombre1',
            'apellido': 'Apellido1',
            'dni': '12345678',
            'fecha_expiracion_dni': timezone.now(),
            'nacionalidad': 'Nacionalidad1',
            'genero': 'Masculino',
            'domicilio': 'Dirección1',
            'fecha_nacimiento': date(1990, 1, 1),
            'cuil_cuit': '20345678901',
        },
        {
            'mail': 'usuario2@mail.com',
            'tipo': 'Usuario',
            'password': 'password2',
            'nombre': 'Nombre2',
            'apellido': 'Apellido2',
            'dni': '23456789',
            'fecha_expiracion_dni': timezone.now(),
            'nacionalidad': 'Nacionalidad2',
            'genero': 'Femenino',
            'domicilio': 'Dirección2',
            'fecha_nacimiento': date(1980, 1, 1),
            'cuil_cuit': '30345678901',
        },
        {
            'mail': 'usuario3@mail.com',
            'tipo': 'Usuario',
            'password': 'password3',
            'nombre': 'Nombre3',
            'apellido': 'Apellido3',
            'dni': '34567890',
            'fecha_expiracion_dni': timezone.now(),
            'nacionalidad': 'Nacionalidad3',
            'genero': 'Masculino',
            'domicilio': 'Dirección3',
            'fecha_nacimiento': date(1970, 1, 1),
            'cuil_cuit': '40345678901',
        },
        {
            'mail': 'usuario4@mail.com',
            'tipo': 'Usuario',
            'password': 'password4',
            'nombre': 'Nombre4',
            'apellido': 'Apellido4',
            'dni': '45678901',
            'fecha_expiracion_dni': timezone.now(),
            'nacionalidad': 'Nacionalidad4',
            'genero': 'Femenino',
            'domicilio': 'Dirección4',
            'fecha_nacimiento': date(1985, 1, 1),
            'cuil_cuit': '50345678901',
        },
        {
            'mail': 'usuario5@mail.com',
            'tipo': 'Usuario',
            'password': 'password5',
            'nombre': 'Nombre5',
            'apellido': 'Apellido5',
            'dni': '56789012',
            'fecha_expiracion_dni': timezone.now(),
            'nacionalidad': 'Nacionalidad5',
            'genero': 'Masculino',
            'domicilio': 'Dirección5',
            'fecha_nacimiento': date(1995, 1, 1),
            'cuil_cuit': '60345678901',
        },
        {
            'mail': 'usuario6@mail.com',
            'tipo': 'Administrador',
            'password': 'password6',
            'nombre': 'Nombre6',
            'apellido': 'Apellido6',
            'dni': '67890123',
            'fecha_expiracion_dni': timezone.now(),
            'nacionalidad': 'Nacionalidad6',
            'genero': 'Femenino',
            'domicilio': 'Dirección6',
            'fecha_nacimiento': date(1975, 1, 1),
            'cuil_cuit': '70345678901',
        },
        {
            'mail': 'usuario7@mail.com',
            'tipo': 'Administrador',
            'password': 'password7',
            'nombre': 'Nombre7',
            'apellido': 'Apellido7',
            'dni': '78901234',
            'fecha_expiracion_dni': timezone.now(),
            'nacionalidad': 'Nacionalidad7',
            'genero': 'Masculino',
            'domicilio': 'Dirección7',
            'fecha_nacimiento': date(1982, 1, 1),
            'cuil_cuit': '80345678901',
        },
        {
            'mail': 'usuario8@mail.com',
            'tipo': 'Administrador',
            'password': 'password8',
            'nombre': 'Nombre8',
            'apellido': 'Apellido8',
            'dni': '89012345',
            'fecha_expiracion_dni': timezone.now(),
            'nacionalidad': 'Nacionalidad8',
            'genero': 'Femenino',
            'domicilio': 'Dirección8',
            'fecha_nacimiento': date(1988, 1, 1),
            'cuil_cuit': '90345678901',
        }, 
    ]
    
    for data in user_data:
        User.objects.create(**data)
        
def inicializar_datos_Embarcaciones(apps, schema_editor):
    Embarcacion = apps.get_model('Register', 'Embarcacion')  # Reemplaza 'tu_app' por el nombre real de tu aplicación Django
    embarcacion_data = [
        {
            'eslora': 10.5,
            'manga': 3.2,
            'calado': 1.8,
            'matricula': 'AB12345',
            'nombre_fantasia': 'Embarcacion1',
            'foto': 'img/b_1.jpeg',
            'dueno_id': 1,  # Assuming the ID of the related user is 1
            'tipo': 'Velero',
        },
        {
            'eslora': 12.0,
            'manga': 4.0,
            'calado': 2.0,
            'matricula': 'CD67890',
            'nombre_fantasia': 'Embarcacion2',
            'foto': 'img/b_2.jpeg',
            'dueno_id': 2,  # Assuming the ID of the related user is 2
            'tipo': 'Yate',
        },
        {
            'eslora': 8.5,
            'manga': 2.5,
            'calado': 1.5,
            'matricula': 'EF54321',
            'nombre_fantasia': 'Embarcacion3',
            'foto': 'img/b_3.jpeg',
            'dueno_id': 3,  # Assuming the ID of the related user is 3
            'tipo': 'Lancha',
        },
        {
            'eslora': 15.0,
            'manga': 5.0,
            'calado': 2.5,
            'matricula': 'GH09876',
            'nombre_fantasia': 'Embarcacion4',
            'foto': 'img/b_4.jpeg',
            'dueno_id': 4,  # Assuming the ID of the related user is 4
            'tipo': 'Barco',
        },
        {
            'eslora': 11.0,
            'manga': 3.5,
            'calado': 2.0,
            'matricula': 'IJ65432',
            'nombre_fantasia': 'Embarcacion5',
            'foto': 'img/b_5.jpeg',
            'dueno_id': 5,  # Assuming the ID of the related user is 5
            'tipo': 'Velero',
        }

        # Agrega más datos de embarcaciones según sea necesario
    ]
    
    for data in embarcacion_data:
        Embarcacion.objects.create(**data)

class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
    name='User',
    fields=[
        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
        ('mail', models.CharField(max_length=150, unique=True)),  # Cambio de username a mail
        ('tipo', models.CharField(max_length=20, choices=[('Administrador', 'Administrador'),
                                                          ('Usuario', 'Usuario'),('Cliente', 'Cliente'),])),
        ('password', models.CharField(max_length=128)),
        ('nombre', models.CharField(max_length=255)),
        ('apellido', models.CharField(max_length=255)),
        ('dni', models.CharField(max_length=20)),
        ('fecha_expiracion_dni', models.DateField()),
        ('nacionalidad', models.CharField(max_length=100)),
        ('genero', models.CharField(max_length=10)),
        ('domicilio', models.CharField(max_length=255)),
        ('fecha_nacimiento', models.DateField()),
        ('cuil_cuit', models.CharField(max_length=20)),
    ],
),
        migrations.CreateModel(
            name='Embarcacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eslora', models.FloatField()),
                ('manga', models.FloatField()),
                ('calado', models.FloatField()),
                ('matricula', models.CharField(max_length=20, unique=True)),
                ('nombre_fantasia', models.CharField(max_length=255)),
                ('foto', models.ImageField(blank=True, null=True, upload_to='embarcaciones/')),
                ('dueno', models.ForeignKey(null=True, on_delete=models.SET_NULL, to='Register.User')),
                ('tipo', models.CharField(choices=[('Velero', 'Velero'), ('Yate', 'Yate'), ('Lancha', 'Lancha'), ('Barco', 'Barco')], max_length=20)),
            ],
        ),
        migrations.RunPython(inicializar_datos_User),
        migrations.RunPython(inicializar_datos_Embarcaciones),
        
    ]
    