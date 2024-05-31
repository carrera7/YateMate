from django.db import models
from Register.models import Embarcacion, User



class Publicacion_Amarra(models.Model):    
    dueño = models.ForeignKey(User, on_delete=models.CASCADE)
    precio = models.TextField()
    fecha_inicio = models.DateField()
    cant_dias= models.TextField()
    ubicacion=models.TextField()

    def __str__(self):
        return self.dueño
    



  

