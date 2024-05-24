from django.shortcuts import render
from Register.models import User
from .models import (Publicacion_ObjetoValioso, Publicacion_Embarcacion, Solicitud_Embarcaciones, Solicitud_ObjetosValiosos , MensajeSolicitudObjetosValiosos , MensajeSolicitudEmbarcaciones, Conversacion, Mensajes_chat)
from Register.models import Embarcacion
from itertools import chain
from django.core.mail import send_mail
from YateMate.settings import EMAIL_HOST_USER
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect


def list_publication(request):
    embarcaciones_vigentes = Publicacion_Embarcacion.objects.filter(estado='Vigente')
    objetos_vigentes = Publicacion_ObjetoValioso.objects.filter(estado='Vigente')
    
    tipo_filtro = request.GET.get('tipo', 'objetos valiosos')  # Valor por defecto 'objetos valiosos'
    
    if tipo_filtro == 'objetos valiosos':
        objetos = objetos_vigentes
    elif tipo_filtro == 'embarcaciones':
        objetos = embarcaciones_vigentes
        
    tipo_objetos = 'Objetos Valiosos' if tipo_filtro == 'objetos valiosos' else 'Embarcaciones'
    
    return render(request, "list_publication.html", {'objetos': objetos , 'tipo_objetos': tipo_objetos,})

# se necesita autenticarse
def list_publication_boat(request):
    embarcaciones_vigentes = Publicacion_Embarcacion.objects.filter(estado='Vigente')
    return render(request, "list_publication_boat.html", {'embarcaciones_vigentes': embarcaciones_vigentes,'tipo_objetos': 'Embarcaciones',})

def list(request):
    objetos_valiosos = Publicacion_ObjetoValioso.objects.all()
    embarcaciones = Publicacion_Embarcacion.objects.all()

    # Obtener el filtro de tipo y estado de la solicitud GET
    tipo_filtro = request.GET.get('tipo','objetos valiosos')  # Valor por defecto 'objetos valiosos'
    estado_filtro = request.GET.get('estado','Vigente')  # Valor por defecto 'Vigente'

    if tipo_filtro == " ":
        tipo_filtro = 'objetos valiosos'
    if estado_filtro == " ":
          estado_filtro = 'Vigente'   
            
    # Filtrar objetos_valiosos y embarcaciones según el tipo y estado seleccionados
    if tipo_filtro == 'objetos valiosos':
        objetos = objetos_valiosos.filter(estado=estado_filtro)
    elif tipo_filtro == 'embarcaciones':
        objetos = embarcaciones.filter(estado=estado_filtro)

    # Agregar el tipo al contexto para pasarlo al HTML
    tipo_objetos = 'Objetos Valiosos' if tipo_filtro == 'objetos valiosos' else 'Embarcaciones'

    # Renderizar el HTML con los datos filtrados o no
    return render(request, 'list.html', {
        'objetos': objetos,
        'tipo_objetos': tipo_objetos,
    })
    
def mis_publicaciones(request):
    
    user_id = request.session['user_id']
    
    objetos = Publicacion_ObjetoValioso.objects.filter(dueño=user_id)
    embarcaciones = Publicacion_Embarcacion.objects.filter(embarcacion__dueno_id=user_id)

    objetos_con_solicitudes = []
    embarcaciones_con_solicitudes = []

    for objeto in objetos:
        tiene_solicitudes = Solicitud_ObjetosValiosos.objects.filter(publicacion=objeto).exists()
        if tiene_solicitudes:
            objetos_con_solicitudes.append(objeto.id)

    for embarcacion in embarcaciones:
        tiene_solicitudes = Solicitud_Embarcaciones.objects.filter(publicacion=embarcacion).exists()
        if tiene_solicitudes:
            embarcaciones_con_solicitudes.append(embarcacion.id)

    return render(request, "ver_mis_publicaciones.html", {
        'objetos': objetos,
        'embarcaciones': embarcaciones,
        'objetos_con_solicitudes': objetos_con_solicitudes,
        'embarcaciones_con_solicitudes': embarcaciones_con_solicitudes,
    })
 
def solicitudes_trueque_objeto(request, publicacion_id):
    # Obtener la publicación de objeto valioso
    publicacion = Publicacion_ObjetoValioso.objects.get(id=publicacion_id)

    # Obtener todas las solicitudes relacionadas con esta publicación
    solicitudes = Solicitud_ObjetosValiosos.objects.filter(publicacion=publicacion)
    
    # Obtener los mensajes para cada solicitud
    solicitudes_con_mensajes = []
    for solicitud in solicitudes:
        mensajes = MensajeSolicitudObjetosValiosos.objects.filter(solicitud_objeto_valioso=solicitud)
        solicitudes_con_mensajes.append((solicitud, mensajes))
    
    tipo = "objetos valiosos"
    context = {
        'solicitudes_con_mensajes': solicitudes_con_mensajes,
        'tipoObj': tipo,
    }
    return render(request, "ver_solicitudes_trueque.html", context)

def solicitudes_trueque_embarcacion(request, publicacion_id):
    # Obtener la publicación de embarcación
    publicacion = Publicacion_Embarcacion.objects.get(id=publicacion_id)

    # Obtener todas las solicitudes relacionadas con esta publicación
    solicitudes = Solicitud_Embarcaciones.objects.filter(publicacion=publicacion)
    
    # Obtener los mensajes para cada solicitud
    solicitudes_con_mensajes = []
    for solicitud in solicitudes:
        mensajes = MensajeSolicitudEmbarcaciones.objects.filter(solicitud_embarcacion=solicitud)
        solicitudes_con_mensajes.append((solicitud, mensajes))
    
    tipo = "embarcaciones"
    context = {
        'solicitudes_con_mensajes': solicitudes_con_mensajes,
        'tipoObj': tipo,
    }
    return render(request, "ver_solicitudes_trueque.html", context)

def rechazar_trueque(request, solicitud_id, tipo):
    if tipo == "objetos valiosos":
        solicitudO = Solicitud_ObjetosValiosos.objects.get(id=solicitud_id)
        dueño = solicitudO.publicacion.dueño
        nombre_objeto_embarcacion = solicitudO.publicacion.marca
        publicacion = solicitudO.publicacion
        solicitudO.delete()
        solicitudes = Solicitud_ObjetosValiosos.objects.filter(publicacion=publicacion)
        # Obtener los mensajes para cada solicitud
        solicitudes_con_mensajes = []
        for solicitud in solicitudes:
            mensajes = MensajeSolicitudObjetosValiosos.objects.filter(solicitud_objeto_valioso=solicitud)
            solicitudes_con_mensajes.append((solicitud, mensajes))
        
        tipo = "objetos valiosos"
        context = {
            'solicitudes_con_mensajes': solicitudes_con_mensajes,
            'tipoObj': tipo,
        }
    else:
        solicitudE = Solicitud_Embarcaciones.objects.get(id=solicitud_id)
        dueño = solicitudE.publicacion.embarcacion.dueno
        nombre_objeto_embarcacion = solicitudE.publicacion.embarcacion.nombre_fantasia
        publicacion = solicitudE.publicacion
        solicitudE.delete()
        solicitudes = Solicitud_Embarcaciones.objects.filter(publicacion=publicacion)
        # Obtener los mensajes para cada solicitud
        solicitudes_con_mensajes = []
        for solicitud in solicitudes:
            mensajes = MensajeSolicitudEmbarcaciones.objects.filter(solicitud_embarcacion=solicitud)
            solicitudes_con_mensajes.append((solicitud, mensajes))
        
        tipo = "embarcaciones"
        context = {
            'solicitudes_con_mensajes': solicitudes_con_mensajes,
            'tipoObj': tipo,
        }
    if dueño.mail:
        subject = 'Actualizacion solicitud de trueque'
        message = f'La solicitud hecha para el trueque { nombre_objeto_embarcacion } fue rechazada'
        send_mail(subject, message, EMAIL_HOST_USER, [dueño.mail])

    return render(request, "ver_solicitudes_trueque.html", context)

def solisitar_trueque(request, publicacion_id,tipo):
    if tipo == "Embarcaciones":
        publicacion = Publicacion_Embarcacion.objects.get(id=publicacion_id)
    else:
        publicacion = Publicacion_ObjetoValioso.objects.get(id=publicacion_id)        
    return render(request, 'solisitar_trueque.html', {'objeto': publicacion, 'tipo_objetos': tipo})

def solicitud_embarcacion(request, publicacion_id):
    user_id = request.session['user_id']
    user = get_object_or_404(User, id=user_id)
    mensaje_solicitud = request.GET.get('mensaje_solicitud', '')  # Obtener el mensaje de la URL
    publicacion = get_object_or_404(Publicacion_Embarcacion, id=publicacion_id)
    
    if Solicitud_Embarcaciones.objects.filter(publicacion=publicacion, usuario_interesado=user).exists():
        mensaje = 'Ya tienes una solicitud previa de esta publicación.'
    else:
        solicitud = Solicitud_Embarcaciones.objects.create(publicacion=publicacion, usuario_interesado=user)
        # Crear el mensaje asociado a la solicitud
        MensajeSolicitudEmbarcaciones.objects.create(mensaje=mensaje_solicitud, solicitud_embarcacion=solicitud)
        mensaje = 'La solicitud fue exitosa.'
        
        # Enviar correo electrónico al dueño de la publicación
        if publicacion.embarcacion.dueno and publicacion.embarcacion.dueno.mail:
            subject = 'Nueva solicitud de trueque'
            message = f'Hola {publicacion.embarcacion.dueno.nombre}, tienes una nueva solicitud de trueque para tu embarcación {publicacion.embarcacion.nombre_fantasia}. Revisa tu perfil en YateMate.'
            send_mail(subject, message,EMAIL_HOST_USER, [publicacion.embarcacion.dueno.mail])
    
    return render(request, 'ver_mas.html', {'objeto': publicacion, 'tipo_objetos': 'Embarcaciones', 'mensaje': mensaje})

def solicitud_objeto_valioso(request, publicacion_id):
    user_id = request.session['user_id']
    user = get_object_or_404(User, id=user_id)
    mensaje_solicitud = request.GET.get('mensaje_solicitud', '')  # Obtener el mensaje de la URL
    publicacion = get_object_or_404(Publicacion_ObjetoValioso, id=publicacion_id)
    
    if Solicitud_ObjetosValiosos.objects.filter(publicacion=publicacion, usuario_interesado=user).exists():
        mensaje = 'Ya tienes una solicitud previa de esta publicación.'
    else:
        solicitud = Solicitud_ObjetosValiosos.objects.create(publicacion=publicacion, usuario_interesado=user)
        # Crear el mensaje asociado a la solicitud
        MensajeSolicitudObjetosValiosos.objects.create(mensaje=mensaje_solicitud, solicitud_objeto_valioso=solicitud)
        mensaje = 'La solicitud fue exitosa.'
        
        # Enviar correo electrónico al dueño de la publicación
        if publicacion.dueño and publicacion.dueño.mail:
            subject = 'Nueva solicitud de trueque'
            message = f'Hola {publicacion.dueño.nombre}, tienes una nueva solicitud de trueque para tu objeto valioso {publicacion.tipo}. Revisa tu perfil en YateMate.'
            send_mail(subject, message,EMAIL_HOST_USER, [publicacion.dueño.mail])
    
    return render(request, 'ver_mas.html', {'objeto': publicacion, 'tipo_objetos': 'Objetos Valiosos', 'mensaje': mensaje})

def saber_mas(request, id, tipo_objetos):    
    # Dependiendo del tipo de objeto, obtén la publicación correspondiente
    if tipo_objetos == 'Objetos Valiosos':
        objeto = Publicacion_ObjetoValioso.objects.get(id=id)
    elif tipo_objetos == 'Embarcaciones':
        objeto = Publicacion_Embarcacion.objects.get(id=id)
    else:
        # Manejar el caso en el que el tipo de objeto no sea válido
        return render(request, 'error.html', {'mensaje': 'Tipo de objeto no válido'})

    return render(request, 'ver_mas.html', {'objeto': objeto, 'tipo_objetos': tipo_objetos})

def eliminarObjeto(request, id):
    # Eliminar el objeto valioso
    objeto = Publicacion_ObjetoValioso.objects.get(id=id)
    
    # Obtener todas las solicitudes relacionadas con el objeto valioso
    solicitudes_objetos_valiosos = Solicitud_ObjetosValiosos.objects.filter(publicacion=objeto)
    
    # Obtener la lista de usuarios que hicieron solicitudes al objeto valioso
    usuarios_interesados = User.objects.filter(solicitudes_objetos_valiosos__in=solicitudes_objetos_valiosos).distinct()
        
    # Enviar correo electrónico a los usuarios que hicieron solicitudes al objeto valioso
    for usuario in usuarios_interesados:
        subject = f'Eliminación de publicación {objeto.tipo}'
        message = f'Hola {usuario},\n\nLa publicación {objeto.tipo} ha sido eliminada.\n\nAtentamente,\nEquipo de YateMate'
        send_mail(subject, message, EMAIL_HOST_USER, [usuario])
        
    
    # Eliminar todas las solicitudes relacionadas con el objeto valioso
    solicitudes_objetos_valiosos.delete()
    objeto.delete()
    
    # Obtener las publicaciones del usuario actual
    objetos = Publicacion_ObjetoValioso.objects.filter(dueño=request.session['user_id'])
    embarcaciones = Publicacion_Embarcacion.objects.filter(embarcacion__dueno=request.session['user_id'])
    
    return render(request, "ver_mis_publicaciones.html", {'objetos': objetos, 'embarcaciones': embarcaciones})

def eliminarEmbarcacion(request, id):
    # Eliminar la embarcación
    embarcacion = Publicacion_Embarcacion.objects.get(id=id)
    
    # Obtener todas las solicitudes relacionadas con la embarcación
    solicitudes_embarcaciones = Solicitud_Embarcaciones.objects.filter(publicacion=embarcacion)

    # Obtener la lista de usuarios que hicieron solicitudes a la embarcación
    usuarios_interesados = User.objects.filter(solicitudes_embarcaciones__in=solicitudes_embarcaciones).distinct()

    # Enviar correo electrónico a los usuarios que hicieron solicitudes a la embarcación
    for usuario in usuarios_interesados:
        subject = f'Eliminación de embarcación {embarcacion.descripcion}'
        message = f'Hola {usuario},\n\nLa embarcación {embarcacion.descripcion} ha sido eliminada.\n\nAtentamente,\nEquipo de YateMate'
        send_mail(subject, message, EMAIL_HOST_USER, [usuario])
    
    # Eliminar todas las solicitudes relacionadas con la embarcación
    solicitudes_embarcaciones.delete()
    embarcacion.delete()
    
    # Obtener las publicaciones del usuario actual
    objetos = Publicacion_ObjetoValioso.objects.filter(dueño=request.session['user_id'])
    embarcaciones = Publicacion_Embarcacion.objects.filter(embarcacion__dueno=request.session['user_id'])
    
    return render(request, "ver_mis_publicaciones.html", {'objetos': objetos, 'embarcaciones': embarcaciones})


def iniciar_solicitud_de_trueque(request, solicitudID, publicacionID, tipo_objetos):
    # Obtener el modelo de publicación y solicitud correcto según el tipo de objetos
    if tipo_objetos == 'Objetos Valiosos':
        publicacion_modelo = Publicacion_ObjetoValioso
        solicitud_modelo = Solicitud_ObjetosValiosos
        respuesta = solicitudes_trueque_objeto(request, publicacionID)
    else:
        publicacion_modelo = Publicacion_Embarcacion
        solicitud_modelo = Solicitud_Embarcaciones
        respuesta = solicitudes_trueque_embarcacion(request, publicacionID)

    # Obtener la publicación y la solicitud
    publicacion = publicacion_modelo.objects.get(id=publicacionID)
    solicitud = solicitud_modelo.objects.get(id=solicitudID)

    # Cambiar el estado de la solicitud
    solicitud.iniciado = True
    solicitud.save()

    # Crear u obtener la conversación entre los usuarios involucrados
    usuario_interesado = solicitud.usuario_interesado
    dueño_publicacion = publicacion.embarcacion.dueno
    conversacion, creado = Conversacion.objects.get_or_create(
        dueño_publicacion=dueño_publicacion,
        solicitante=usuario_interesado
    )

    # Crear el mensaje en la conversación
    mensaje_solicitud = f"Hola {usuario_interesado.nombre}, estoy interesado para hacer un trueque"
    mensaje = Mensajes_chat.objects.create(
        conversacion=conversacion,
        sender=dueño_publicacion,
        mensaje_texto=mensaje_solicitud
    )

    # Cambiar el estado de la publicación
    publicacion.estado = "Proceso"
    publicacion.save()

    return respuesta





