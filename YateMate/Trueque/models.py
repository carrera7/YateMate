from django.db import models
from Register.models import Embarcacion, User

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
    foto = models.ImageField(upload_to='img_pu/')

    def __str__(self):
        return f"{self.tipo} - {self.marca}"
       
#Embarcaciones
class Publicacion_Embarcacion(models.Model):
    ESTADO_CHOICES = (
        ('Vigente', 'Vigente'),
        ('Proceso', 'Proceso'),
        ('Finalizado', 'Finalizado'),
    )
    embarcacion = models.ForeignKey(Embarcacion, on_delete=models.CASCADE)
    descripcion = models.TextField()
    estado = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre_fantasia

class Solicitud_Embarcaciones(models.Model):
    publicacion = models.ForeignKey('Publicacion_Embarcacion', on_delete=models.CASCADE)
    usuarios_interesados = models.ManyToManyField(User, related_name='solicitudes_embarcaciones')


class Solicitud_ObjetosValiosos(models.Model):
    publicacion = models.ForeignKey('Publicacion_ObjetoValioso', on_delete=models.CASCADE)
    usuarios_interesados = models.ManyToManyField(User, related_name='solicitudes_objetos_valiosos')
