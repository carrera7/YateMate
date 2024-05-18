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
    dueño = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
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
    publicacion = models.ForeignKey(Publicacion_Embarcacion, on_delete=models.CASCADE)
    usuario_interesado = models.ForeignKey(User, on_delete=models.CASCADE, related_name='solicitudes_embarcaciones')
    
    def __str__(self):
        return f'Solicitud de {self.usuario_interesado} para {self.publicacion}'

class Solicitud_ObjetosValiosos(models.Model):
    publicacion = models.ForeignKey(Publicacion_ObjetoValioso, on_delete=models.CASCADE)
    usuario_interesado = models.ForeignKey(User, on_delete=models.CASCADE, related_name='solicitudes_objetos_valiosos')
    
    def __str__(self):
        return f'Solicitud de {self.usuario_interesado} para {self.publicacion}'
    
class MensajeSolicitudObjetosValiosos(models.Model):
    mensaje = models.TextField()
    solicitud_objeto_valioso = models.ForeignKey('Solicitud_ObjetosValiosos', on_delete=models.CASCADE)

class MensajeSolicitudEmbarcaciones(models.Model):
    mensaje = models.TextField()
    solicitud_embarcacion = models.ForeignKey('Solicitud_Embarcaciones', on_delete=models.CASCADE)