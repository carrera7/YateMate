from django.db import models
from Register.models import Embarcacion, User



class Publicacion_Amarra(models.Model):
    ESTADOS = (
        ('Vigente', 'Vigente'),
        ('En Proceso', 'En Proceso'),
        ('Finalizado', 'Finalizado'),
    )

    dueño = models.ForeignKey(User, on_delete=models.CASCADE)
    precio = models.TextField()
    fecha_inicio = models.DateField()
    cant_dias = models.TextField()
    ubicacion = models.TextField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='Vigente')

    def __str__(self):
        return f"{self.dueño} - {self.estado}"

    


class Reserva(models.Model):
    publicacion = models.ForeignKey(Publicacion_Amarra, on_delete=models.CASCADE)
    fecha_ingreso = models.DateField(null=True)
    fecha_salida = models.DateField(null=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Reserva de {self.usuario} para {self.publicacion}'
  

