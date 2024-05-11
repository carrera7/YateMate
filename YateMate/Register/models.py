from django.db import models
from django.contrib.auth.models import AbstractUser

# Modelo de iformacion asosicada al usuario
class Usuario(models.Model):
    TIPOS = (
        ('Administrador', 'Administrador'),
        ('Usuario', 'Usuario'),
    )

    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    dni = models.CharField(max_length=20)
    fecha_expiracion_dni = models.DateField()
    nacionalidad = models.CharField(max_length=100)
    genero = models.CharField(max_length=10)
    domicilio = models.CharField(max_length=255)
    fecha_nacimiento = models.DateField()
    cuil_cuit = models.CharField(max_length=20)
    tipo = models.CharField(max_length=20, choices=TIPOS)

    def __str__(self):
        return f'{self.nombre} {self.apellido}'

class Embarcacion(models.Model):
    TIPOS = (
        ('Velero', 'Velero'),
        ('Yate', 'Yate'),
        ('Lancha', 'Lancha'),
        ('Barco', 'Barco'),
    )

    eslora = models.FloatField()
    manga = models.FloatField()
    calado = models.FloatField()
    matricula = models.CharField(max_length=20, unique=True)
    nombre_fantasia = models.CharField(max_length=255)
    foto = models.ImageField(upload_to='embarcaciones/', null=True, blank=True)
    dueno = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)

    tipo = models.CharField(max_length=20, choices=TIPOS)

    def __str__(self):
        return f'{self.nombre_fantasia} - {self.matricula}'
    
class User(models.Model):
    # Definimos el modelo Usuario que tendrá tres campos: username, datos (clave foránea) y password.
    username = models.CharField(max_length=150, unique=True)  # Nombre de usuario (email).
    datos = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True)  # Clave foránea a UsuarioDatos.
    password = models.CharField(max_length=128)  # Contraseña.