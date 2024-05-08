from django.db import models
# Create your models here.
"""
class Usuario(models.Model):
    # Definición del modelo Usuario
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    # Otros campos según tus necesidades
    
    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Articulo(models.Model):
    # Definición del modelo Articulo
    TIPOS = [
        ('electronico', 'Electrónico'),
        ('ropa', 'Ropa'),
        ('hogar', 'Hogar'),
        # Agrega más tipos según tus necesidades
    ]
    
    tipo = models.CharField(max_length=20, choices=TIPOS)
    marca = models.CharField(max_length=100)
    descripcion = models.TextField()
    estado = models.CharField(max_length=20)
    dueño = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.tipo} - {self.marca} - {self.descripcion[:20]}..."
"""
#ObjetoValioso
class Publicacion_ObjetoValioso(models.Model):
    ESTADO_CHOICES = (
        ('Vigente', 'Vigente'),
        ('Proceso', 'Proceso'),
        ('Finalizado', 'Finalizado'),
    )

    tipo = models.CharField(max_length=100)
    marca = models.CharField(max_length=100)
    descripcion = models.TextField()
    estado = models.CharField(max_length=50)
    dueño = models.IntegerField()
    foto = models.ImageField(upload_to='productos_fotos/')

    def __str__(self):
        return f"{self.tipo} - {self.marca}"
    
    
#Embarcaciones
class Publicacion_Embarcacion(models.Model):
    ESTADO_CHOICES = (
        ('Vigente', 'Vigente'),
        ('Proceso', 'Proceso'),
        ('Finalizado', 'Finalizado'),
    )

    tipo = models.CharField(max_length=100)
    eslora = models.DecimalField(max_digits=5, decimal_places=2)
    manga = models.DecimalField(max_digits=5, decimal_places=2)
    calado = models.DecimalField(max_digits=5, decimal_places=2)
    matricula = models.CharField(max_length=20)
    nombre_fantasia = models.CharField(max_length=100)
    foto = models.ImageField(upload_to='barcos_fotos/')
    dueño = models.IntegerField()

    def __str__(self):
        return self.nombre_fantasia
