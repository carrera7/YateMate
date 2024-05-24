from django.conf import settings

from .models import Mensajes_chat

from .models import Conversacion

def conversaciones_usuario(request):
    user_id = request.session.get('user_id')
    if user_id:
        conversaciones = Conversacion.objects.filter(dueño_publicacion=user_id)
        return {'conversaciones_usuario': conversaciones}
    else:
        return {'conversaciones_usuario': []}
