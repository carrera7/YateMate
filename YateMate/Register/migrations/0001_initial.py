from django.db import migrations, models
from datetime import date

def inicializar_datos_Usuarios(apps, schema_editor):
    Usuario = apps.get_model('Register', 'Usuario')  # Replace 'your_app_name' with your actual Django app name
    
    user_data = [
        {
            'nombre': 'Usuario1',
            'apellido': 'Apellido1',
            'dni': '1234567890',
            'fecha_expiracion_dni': date(2025, 12, 31),
            'nacionalidad': 'Nacionalidad1',
            'genero': 'Masculino',
            'domicilio': 'Dirección1',
            'fecha_nacimiento': date(1990, 1, 1),
            'cuil_cuit': '12345678901',
            'tipo': 'Usuario',
        },
        {
            'nombre': 'Usuario2',
            'apellido': 'Apellido2',
            'dni': '2345678901',
            'fecha_expiracion_dni': date(2026, 12, 31),
            'nacionalidad': 'Nacionalidad2',
            'genero': 'Femenino',
            'domicilio': 'Dirección2',
            'fecha_nacimiento': date(1995, 5, 15),
            'cuil_cuit': '23456789012',
            'tipo': 'Usuario',
        },
        {
            'nombre': 'Usuario3',
            'apellido': 'Apellido3',
            'dni': '3456789012',
            'fecha_expiracion_dni': date(2027, 12, 31),
            'nacionalidad': 'Nacionalidad3',
            'genero': 'Masculino',
            'domicilio': 'Dirección3',
            'fecha_nacimiento': date(1988, 8, 8),
            'cuil_cuit': '34567890123',
            'tipo': 'Usuario',
        },
        {
            'nombre': 'Administrador1',
            'apellido': 'ApellidoAdmin1',
            'dni': '4567890123',
            'fecha_expiracion_dni': date(2028, 12, 31),
            'nacionalidad': 'NacionalidadAdmin1',
            'genero': 'Femenino',
            'domicilio': 'DirecciónAdmin1',
            'fecha_nacimiento': date(1978, 3, 8),
            'cuil_cuit': '45678901234',
            'tipo': 'Administrador',
        },
        {
            'nombre': 'NuevoUsuario1',
            'apellido': 'NuevoApellido1',
            'dni': '0987654321',
            'fecha_expiracion_dni': date(2025, 11, 30),
            'nacionalidad': 'NuevaNacionalidad1',
            'genero': 'Femenino',
            'domicilio': 'NuevaDirección1',
            'fecha_nacimiento': date(1992, 4, 10),
            'cuil_cuit': '09876543210',
            'tipo': 'Usuario',
        },
        {
            'nombre': 'NuevoUsuario2',
            'apellido': 'NuevoApellido2',
            'dni': '9876543210',
            'fecha_expiracion_dni': date(2026, 10, 30),
            'nacionalidad': 'NuevaNacionalidad2',
            'genero': 'Masculino',
            'domicilio': 'NuevaDirección2',
            'fecha_nacimiento': date(1988, 8, 20),
            'cuil_cuit': '98765432101',
            'tipo': 'Usuario',
        },
        {
            'nombre': 'NuevoUsuario3',
            'apellido': 'NuevoApellido3',
            'dni': '8765432109',
            'fecha_expiracion_dni': date(2027, 9, 30),
            'nacionalidad': 'NuevaNacionalidad3',
            'genero': 'Femenino',
            'domicilio': 'NuevaDirección3',
            'fecha_nacimiento': date(1995, 3, 5),
            'cuil_cuit': '87654321098',
            'tipo': 'Usuario',
        },
        {
            'nombre': 'NuevoUsuario4',
            'apellido': 'NuevoApellido4',
            'dni': '7654321098',
            'fecha_expiracion_dni': date(2028, 8, 30),
            'nacionalidad': 'NuevaNacionalidad4',
            'genero': 'Masculino',
            'domicilio': 'NuevaDirección4',
            'fecha_nacimiento': date(1990, 11, 15),
            'cuil_cuit': '76543210987',
            'tipo': 'Usuario',
        },
        {
            'nombre': 'NuevoUsuario5',
            'apellido': 'NuevoApellido5',
            'dni': '6543210987',
            'fecha_expiracion_dni': date(2029, 7, 30),
            'nacionalidad': 'NuevaNacionalidad5',
            'genero': 'Femenino',
            'domicilio': 'NuevaDirección5',
            'fecha_nacimiento': date(1983, 6, 25),
            'cuil_cuit': '65432109876',
            'tipo': 'Usuario',
        },

        {
            'nombre': 'Administrador2',
            'apellido': 'ApellidoAdmin2',
            'dni': '5678901234',
            'fecha_expiracion_dni': date(2029, 12, 31),
            'nacionalidad': 'NacionalidadAdmin2',
            'genero': 'Masculino',
            'domicilio': 'DirecciónAdmin2',
            'fecha_nacimiento': date(1983, 12, 12),
            'cuil_cuit': '56789012345',
            'tipo': 'Administrador',
        },
        {
            'nombre': 'Administrador3',
            'apellido': 'ApellidoAdmin3',
            'dni': '6789012345',
            'fecha_expiracion_dni': date(2030, 12, 31),
            'nacionalidad': 'NacionalidadAdmin3',
            'genero': 'Femenino',
            'domicilio': 'DirecciónAdmin3',
            'fecha_nacimiento': date(1990, 5, 5),
            'cuil_cuit': '67890123456',
            'tipo': 'Administrador',
        },
    ]
    
    for data in user_data:
        Usuario.objects.create(**data)
        
def inicializar_datos_User(apps, schema_editor):
    User = apps.get_model('Register', 'User')  # Reemplaza 'tu_app' con el nombre real de tu aplicación Django
    Usuario = apps.get_model('Register', 'Usuario')  # Reemplaza 'tu_app' con el nombre real de tu aplicación Django
    
    usuario_instance_1 = Usuario.objects.get(id=1)  # Obtiene una instancia existente de Usuario
    usuario_instance_2 = Usuario.objects.get(id=2)  # Obtiene una instancia existente de Usuario
    usuario_instance_3 = Usuario.objects.get(id=3)  # Obtiene una instancia existente de Usuario
    usuario_instance_4 = Usuario.objects.get(id=4)  # Obtiene una instancia existente de Usuario
    usuario_instance_5 = Usuario.objects.get(id=5)  # Obtiene una instancia existente de Usuario
    
    user_data = [
        {
            'username': 'usuario1@mail.com',
            'datos': usuario_instance_1,  # Aquí debes poner la clave foránea a otro Usuario si es relevante para tu aplicación
            'password': 'password1',
        },
        {
            'username': 'usuario2@mail.com',
            'datos': usuario_instance_2,
            'password': 'password2',
        },
        {
            'username': 'usuario3@mail.com',
            'datos': usuario_instance_3,
            'password': 'password3',
        },
        {
            'username': 'usuario4@mail.com',
            'datos': usuario_instance_4,
            'password': 'password4',
        },
        {
            'username': 'usuario5@mail.com',
            'datos': usuario_instance_5,
            'password': 'password5',
        },
    ]
    
    for data in user_data:
        User.objects.create(**data)
        
def inicializar_datos_Embarcaciones(apps, schema_editor):
    Embarcacion = apps.get_model('Register', 'Embarcacion')  # Reemplaza 'tu_app' por el nombre real de tu aplicación Django
    Usuario = apps.get_model('Register', 'Usuario')
    embarcacion_data = [
        {
            'eslora': 10.5,
            'manga': 3.2,
            'calado': 1.8,
            'matricula': 'AB12345',
            'nombre_fantasia': 'Embarcacion1',
            'foto': 'embarcaciones/foto1.jpg',
            'dueno_id': 1,  # Assuming the ID of the related user is 1
            'tipo': 'Velero',
        },
        {
            'eslora': 12.0,
            'manga': 4.0,
            'calado': 2.0,
            'matricula': 'CD67890',
            'nombre_fantasia': 'Embarcacion2',
            'foto': 'embarcaciones/foto2.jpg',
            'dueno_id': 2,  # Assuming the ID of the related user is 2
            'tipo': 'Yate',
        },
        {
            'eslora': 8.5,
            'manga': 2.5,
            'calado': 1.5,
            'matricula': 'EF54321',
            'nombre_fantasia': 'Embarcacion3',
            'foto': 'embarcaciones/foto3.jpg',
            'dueno_id': 3,  # Assuming the ID of the related user is 3
            'tipo': 'Lancha',
        },
        {
            'eslora': 15.0,
            'manga': 5.0,
            'calado': 2.5,
            'matricula': 'GH09876',
            'nombre_fantasia': 'Embarcacion4',
            'foto': 'embarcaciones/foto4.jpg',
            'dueno_id': 4,  # Assuming the ID of the related user is 4
            'tipo': 'Barco',
        },
        {
            'eslora': 11.0,
            'manga': 3.5,
            'calado': 2.0,
            'matricula': 'IJ65432',
            'nombre_fantasia': 'Embarcacion5',
            'foto': 'embarcaciones/foto5.jpg',
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
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('apellido', models.CharField(max_length=255)),
                ('dni', models.CharField(max_length=20)),
                ('fecha_expiracion_dni', models.DateField()),
                ('nacionalidad', models.CharField(max_length=100)),
                ('genero', models.CharField(max_length=10)),
                ('domicilio', models.CharField(max_length=255)),
                ('fecha_nacimiento', models.DateField()),
                ('cuil_cuit', models.CharField(max_length=20)),
                ('tipo', models.CharField(choices=[('Administrador', 'Administrador'), ('Usuario', 'Usuario')], max_length=20)),
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
                ('dueno', models.ForeignKey(null=True, on_delete=models.SET_NULL, to='Register.Usuario')),
                ('tipo', models.CharField(choices=[('Velero', 'Velero'), ('Yate', 'Yate'), ('Lancha', 'Lancha'), ('Barco', 'Barco')], max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=150, unique=True)),
                ('datos', models.ForeignKey(null=True, on_delete=models.SET_NULL, to='Register.Usuario')),
                ('password', models.CharField(max_length=128)),
            ],
        ),
        migrations.RunPython(inicializar_datos_Usuarios),
        migrations.RunPython(inicializar_datos_Embarcaciones),
        migrations.RunPython(inicializar_datos_User),
    ]