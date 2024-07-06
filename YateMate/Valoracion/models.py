from django.db import models
from Register.models import User
from Trueque.models import Publicacion_ObjetoValioso, Publicacion_Embarcacion
from Amarra.models import Publicacion_Amarra

# Modelo de Valoración Trueque
class Valoracion_Trueque(models.Model):
    ESTADO_VALORACION_CHOICES = (
        ('Inicio', 'Inicio'),
        ('Proceso', 'Proceso'),
        ('Finalizado', 'Finalizado'),
    )
    TIPO_PUBLICACION_CHOICES = (
        ('ObjetoValioso', 'Objeto Valioso'),
        ('Embarcacion', 'Embarcación'),
    )

    tipo_publicacion = models.CharField(max_length=20, choices=TIPO_PUBLICACION_CHOICES)
    publicacion_objeto_valioso = models.ForeignKey(Publicacion_ObjetoValioso, on_delete=models.CASCADE, null=True, blank=True)
    publicacion_embarcacion = models.ForeignKey(Publicacion_Embarcacion, on_delete=models.CASCADE, null=True, blank=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    estrellas = models.IntegerField()
    comentario = models.TextField()
    estado = models.CharField(max_length=50, choices=ESTADO_VALORACION_CHOICES)
    dueño = models.ForeignKey(User, on_delete=models.CASCADE, related_name='valoraciones_trueque')
    respuesta = models.TextField()

    def __str__(self):
        publicacion_str = self.get_publicacion_display()
        return f"Valoración de {publicacion_str} por {self.usuario}"

    def get_publicacion_display(self):
        if self.tipo_publicacion == 'ObjetoValioso' and self.publicacion_objeto_valioso:
            return f"Objeto Valioso: {self.publicacion_objeto_valioso}"
        elif self.tipo_publicacion == 'Embarcacion' and self.publicacion_embarcacion:
            return f"Embarcación: {self.publicacion_embarcacion}"
        else:
            return 'Publicación desconocida'

    def save(self, *args, **kwargs):
        if self.tipo_publicacion == 'ObjetoValioso' and self.publicacion_objeto_valioso:
            self.dueño = self.publicacion_objeto_valioso.dueño
        elif self.tipo_publicacion == 'Embarcacion' and self.publicacion_embarcacion:
            self.dueño = self.publicacion_embarcacion.embarcacion.dueno
        super().save(*args, **kwargs)


# Modelo de Valoración Amarra 
class Valoracion_Amarra(models.Model):
    ESTADO_VALORACION_CHOICES = (
        ('Inicio', 'Inicio'),
        ('Proceso', 'Proceso'),
        ('Finalizado', 'Finalizado'),
    )

    publicacion_amarra = models.ForeignKey(Publicacion_Amarra, on_delete=models.CASCADE, null=True, blank=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    estrellas = models.IntegerField()
    comentario = models.TextField()
    estado = models.CharField(max_length=50, choices=ESTADO_VALORACION_CHOICES)
    dueño = models.ForeignKey(User, on_delete=models.CASCADE, related_name='valoraciones_amarra')
    respuesta = models.TextField()
    
    def __str__(self):
        return f"Valoración de la Amarra Ubicacion:{self.publicacion_amarra.ubicacion} , del {self.publicacion_amarra} por {self.usuario}"

    def save(self, *args, **kwargs):
        if self.publicacion_amarra:
            self.dueño = self.publicacion_amarra.dueño
        super().save(*args, **kwargs)
