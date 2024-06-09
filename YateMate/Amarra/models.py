from django.db import models
from django.utils import timezone
from Register.models import Embarcacion, User

class Publicacion_Amarra(models.Model):
    ESTADOS = (
        ('Vigente', 'Vigente'),
        ('En Proceso', 'En Proceso'),
        ('Finalizado', 'Finalizado'),
    )

    dueño = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    precio = models.TextField()
    fecha_inicio = models.DateField()
    cant_dias = models.TextField()
    ubicacion = models.TextField()
    cant_dias_disponibles = models.TextField(null=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='Vigente')

    def __str__(self):
        return f"{self.dueño} - {self.estado}"
    
    def actualizar_dias_disponibles(self):
        hoy = timezone.now().date()
        diferencia_dias = (hoy - self.fecha_inicio).days

        if diferencia_dias > 0:
            # Calculate initial available days
            dias_disponibles = int(float(self.cant_dias)) - diferencia_dias

            # Calculate total reserved days
            reservas = Reserva.objects.filter(publicacion=self)
            total_reserved_days = sum([int(reserva.cant_dias) for reserva in reservas])

            # Update available days
            self.cant_dias_disponibles = str(dias_disponibles - total_reserved_days)
            self.save()

class Reserva(models.Model):
    ESTADOS = (
        ('Vigente', 'Vigente'),
        ('En Proceso', 'En Proceso'),
        ('Finalizado', 'Finalizado'),
    )
    
    publicacion = models.ForeignKey(Publicacion_Amarra, on_delete=models.CASCADE)
    fecha_ingreso = models.DateField(null=True)
    cant_dias = models.TextField()
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='Vigente')

    def __str__(self):
        return f'Reserva de {self.usuario} para {self.publicacion}'