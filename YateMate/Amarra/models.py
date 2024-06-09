from datetime import timedelta
from django.db import models
from django.utils import timezone
from Register.models import Embarcacion, User

class Publicacion_Amarra(models.Model):
    ESTADOS = (
        ('Vigente', 'Vigente'),
        ('En Proceso', 'En Proceso'),
        ('Finalizado', 'Finalizado'),
    )

    dueño = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
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
            dias_disponibles = int(float(self.cant_dias)) - diferencia_dias
            reservas = Reserva.objects.filter(publicacion=self)
            total_reserved_days = sum([int(reserva.cant_dias) for reserva in reservas])
            self.cant_dias_disponibles = str(dias_disponibles - total_reserved_days)
        else:
            self.cant_dias_disponibles = self.cant_dias

        if int(self.cant_dias_disponibles) <= 0:
            self.cant_dias_disponibles = '0'
            self.estado = 'En Proceso'
        else:
            self.estado = 'Vigente'

        self.save()

    def is_available_on(self, date):
        if date < self.fecha_inicio:
            return False

        diferencia_dias = (date - self.fecha_inicio).days
        if diferencia_dias >= float(self.cant_dias):  # Cambio aquí: float en lugar de int
            return False

        reservas = Reserva.objects.filter(publicacion=self)
        for reserva in reservas:
            # Aquí puedes implementar la lógica que necesitas para verificar la disponibilidad de la reserva
            # por ejemplo, si hay un atributo "estado" en Reserva que indica si está vigente
            if reserva.estado == 'Vigente':
                reserva_fecha_fin = reserva.fecha_ingreso + timedelta(days=int(reserva.cant_dias))
                if reserva.fecha_ingreso <= date < reserva_fecha_fin:
                    return False

        return True

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