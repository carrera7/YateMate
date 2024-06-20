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
    matricula = models.CharField(max_length=50)  # Agregado el campo matricula
    dueño = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    foto = models.ImageField(upload_to='static/img_o/')

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
    iniciado = models.BooleanField(default=False)
    
    def __str__(self):
        return f'Solicitud de {self.usuario_interesado} para {self.publicacion}'

class Solicitud_ObjetosValiosos(models.Model):
    publicacion = models.ForeignKey(Publicacion_ObjetoValioso, on_delete=models.CASCADE)
    usuario_interesado = models.ForeignKey(User, on_delete=models.CASCADE, related_name='solicitudes_objetos_valiosos')
    iniciado = models.BooleanField(default=False)

    def __str__(self):
        return f'Solicitud de {self.usuario_interesado} para {self.publicacion}'
    
class MensajeSolicitudObjetosValiosos(models.Model):
    mensaje = models.TextField()
    solicitud_objeto_valioso = models.ForeignKey('Solicitud_ObjetosValiosos', on_delete=models.CASCADE)

class MensajeSolicitudEmbarcaciones(models.Model):
    mensaje = models.TextField()
    solicitud_embarcacion = models.ForeignKey('Solicitud_Embarcaciones', on_delete=models.CASCADE)

class Conversacion(models.Model):
    dueño_publicacion = models.ForeignKey(User, related_name='conversations_initiated', on_delete=models.CASCADE)
    solicitante = models.ForeignKey(User, related_name='conversations_received', on_delete=models.CASCADE)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('dueño_publicacion', 'solicitante')

    def get_mensajes(self):
        return Mensajes_chat.objects.filter(conversacion=self).order_by('enviado_a')

    def get_participantes(self):
        return [self.dueño_publicacion, self.solicitante]

    def __str__(self):
        return f'Conversación entre {self.dueño_publicacion.nombre} y {self.solicitante.nombre}'


class Mensajes_chat(models.Model):
    conversacion = models.ForeignKey(Conversacion, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, to_field='id')
    mensaje_texto = models.TextField()
    enviado_a = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.sender.nombre}: {self.mensaje_texto[:30]}... ({self.enviado_a.strftime("%Y-%m-%d %H:%M:%S")})'

    @classmethod
    def get_ordered_messages(cls, conversation_id):
        return cls.objects.filter(conversacion_id=conversation_id).order_by('enviado_a')


class Denuncia(models.Model):
    denunciado = models.ForeignKey(User, related_name='denuncias_recibidas', on_delete=models.CASCADE)
    denunciante = models.ForeignKey(User, related_name='denuncias_realizadas', on_delete=models.CASCADE)
    mensaje_texto = models.TextField()
    class Meta:
        unique_together = ('denunciado', 'denunciante', 'mensaje_texto')  # Asegura que no se pueda duplicar la misma denuncia

    def __str__(self):
        return f'Denuncia de {self.denunciante.username} contra {self.denunciado.username}'