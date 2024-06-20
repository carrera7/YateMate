from django.contrib import messages
from django.shortcuts import render
from Register.models import User
from .models import (Publicacion_ObjetoValioso, Publicacion_Embarcacion, Solicitud_Embarcaciones, Solicitud_ObjetosValiosos, MensajeSolicitudObjetosValiosos , MensajeSolicitudEmbarcaciones, Conversacion, Mensajes_chat, Denuncia)
from Register.models import Embarcacion
from itertools import chain
from django.core.mail import send_mail
from YateMate.settings import EMAIL_HOST_USER
from YateMate import settings
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from .froms import PublicacionObjetoValiosoForm ,PublicacionEmbarcacionForm
#from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages


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
    # Consultar todas las publicaciones de objetos valiosos y embarcaciones
    objetos_valiosos = Publicacion_ObjetoValioso.objects.all()
    embarcaciones = Publicacion_Embarcacion.objects.all()

    # Obtener el filtro de tipo y estado de la solicitud GET
    tipo_filtro = request.GET.get('tipo', 'objetos valiosos')  # Valor por defecto 'objetos valiosos'
    estado_filtro = request.GET.get('estado', 'Vigente')  # Valor por defecto 'Vigente'

    if tipo_filtro == "":
        tipo_filtro = 'objetos valiosos'
    if estado_filtro == "":
        estado_filtro = 'Vigente'

    # Filtrar objetos_valiosos y embarcaciones según el tipo y estado seleccionados
    if tipo_filtro == 'objetos valiosos':
        objetos = objetos_valiosos.filter(estado=estado_filtro)
    else:
        objetos = embarcaciones.filter(estado=estado_filtro)

    # Agregar el tipo al contexto para pasarlo al HTML
    tipo_objetos = 'Objetos Valiosos' if tipo_filtro == 'objetos valiosos' else 'Embarcaciones'

    # Verificar si se ha finalizado un trueque y recargar las publicaciones si es necesario
    if request.session.get('trueque_finalizado', False):
        del request.session['trueque_finalizado']  # Eliminar la clave de la sesión
        return redirect('list')  # Redirigir para volver a cargar las publicaciones

    user_id = request.session['user_id']
    user = get_object_or_404(User, id=user_id)

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
        subject = 'Solicitud Rechazada'
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

def darDeBajaObjeto(request, publicacion_id):
    publicacion = Publicacion_ObjetoValioso.objects.get(id=publicacion_id)
    # Obtener todas las solicitudes relacionadas con esta publicación
    solicitudes = Solicitud_ObjetosValiosos.objects.filter(publicacion=publicacion)
    # Obtener la lista de usuarios que hicieron solicitudes al objeto valioso
    usuarios_interesados = User.objects.filter(solicitudes_objetos_valiosos__in=solicitudes).distinct()
     # Enviar correo electrónico a los usuarios que hicieron solicitudes al objeto valioso
    if usuarios_interesados:
        for usuario in usuarios_interesados:
            subject = f'Eliminación de publicación {publicacion.tipo}'
            message = f'Se ha dado de baja la publicación/trueque'
            send_mail(subject, message, EMAIL_HOST_USER, [usuario]) 
    else:
        subject = f'Eliminación de publicación {publicacion.tipo}'
        message = f'Se ha dado de baja la publicación/trueque'
        send_mail(subject, message, EMAIL_HOST_USER, [publicacion.embarcacion.dueno.mail]) 
     # Eliminar todas las solicitudes relacionadas a la embarcacion
    solicitudes.delete()
    publicacion.delete()
    mensaje= 'Eliminacion exitosa'
    return render(request, 'ver_mas.html', {'objeto': publicacion, 'tipo_objetos': 'Objetos Valiosos', 'mensaje': mensaje})
    
def darDeBajaEmbarcacion(request,  publicacion_id):
    publicacion= Publicacion_Embarcacion.objects.get(id=publicacion_id)
    # Obtener todas las solicitudes relacionadas con esta publicación
    solicitudes = Solicitud_Embarcaciones.objects.filter(publicacion=publicacion)
    # Obtener la lista de usuarios que hicieron solicitudes a la embarcacion
    usuarios_interesados = User.objects.filter(solicitudes_objetos_valiosos__in=solicitudes).distinct()
    if usuarios_interesados:
        for usuario in usuarios_interesados:
            subject = f'Eliminación de publicación {publicacion.tipo}'
            message = f'Se ha dado de baja la publicación/trueque'
            send_mail(subject, message, EMAIL_HOST_USER, [usuario]) 
    else:
        subject = f'Eliminación de publicación {publicacion.tipo}'
        message = f'Se ha dado de baja la publicación/trueque'
        send_mail(subject, message, EMAIL_HOST_USER, [publicacion.embarcacion.dueno.mail]) 

    # Eliminar todas las solicitudes relacionadas a la embarcacion
    solicitudes.delete()
    publicacion.delete()
    mensaje= 'Eliminacion exitosa'
    return render(request, 'ver_mas.html', {'objeto': publicacion, 'tipo_objetos': 'Embarcacion', 'mensaje': mensaje})

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
    # Verifica el tipo de objeto y asigna los modelos adecuados

    if tipo_objetos == 'embarcaciones':
        publicacion_modelo = Publicacion_Embarcacion
        solicitud_modelo = Solicitud_Embarcaciones
        respuesta = solicitudes_trueque_embarcacion(request, publicacionID)
        mensaje_original = MensajeSolicitudEmbarcaciones.objects.get(solicitud_embarcacion=solicitudID).mensaje
    else:
        publicacion_modelo = Publicacion_ObjetoValioso
        solicitud_modelo = Solicitud_ObjetosValiosos
        respuesta = solicitudes_trueque_objeto(request, publicacionID)
        mensaje_original = MensajeSolicitudObjetosValiosos.objects.get(solicitud_objeto_valioso=solicitudID).mensaje


    # Obtener la publicación y la solicitud
    publicacion = get_object_or_404(publicacion_modelo, id=publicacionID)
    solicitud = get_object_or_404(solicitud_modelo, id=solicitudID)

    # Cambiar el estado de la solicitud
    solicitud.iniciado = True
    solicitud.save()

    # Crear u obtener la conversación entre los usuarios involucrados
    usuario_interesado_id = solicitud.usuario_interesado.id  # Corregido
    usuario_interesado = User.objects.get(id=usuario_interesado_id)
    dueño_publicacion = publicacion.embarcacion.dueno if tipo_objetos == 'embarcaciones' else publicacion.dueño
    conversacion, creado = Conversacion.objects.get_or_create(
        dueño_publicacion=dueño_publicacion,
        solicitante=usuario_interesado
    )

    mensaje = Mensajes_chat.objects.create(
        conversacion=conversacion,
        sender=usuario_interesado,  # Corregido
        mensaje_texto=mensaje_original
    )

    # Crear el mensaje en la conversación
    mensaje_solicitud = f"Hola {usuario_interesado.nombre}, estoy interesado en hacer un trueque"
    mensaje = Mensajes_chat.objects.create(
        conversacion=conversacion,
        sender=dueño_publicacion,
        mensaje_texto=mensaje_solicitud
    )

    # Cambiar el estado de la publicación
    publicacion.estado = "Proceso"
    publicacion.save()

    return respuesta


def enviar_mensaje(request):
    if request.method == 'POST':
        conversacion_id = request.POST.get('conversacion_id')
        mensaje_texto = request.POST.get('mensaje_texto')
        user_id = request.session['user_id']
        user = get_object_or_404(User, id=user_id)
        conversacion = get_object_or_404(Conversacion, id=conversacion_id)
        Mensajes_chat.objects.create(mensaje_texto=mensaje_texto, conversacion=conversacion, sender=user)
    return redirect(request.META.get('HTTP_REFERER', '/'))  # Redirige a la página de conversaciones después de enviar el mensaje

def registrar_Objeto_Valioso(request):
    usuario = User.objects.get(id=request.session['user_id'])  # Asegúrate de que el usuario esté autenticado

    if request.method == 'POST':
        form = PublicacionObjetoValiosoForm(usuario, request.POST, request.FILES)
        if form.is_valid():
            # Validar si ya existe una publicación con la misma matrícula
            matricula = form.cleaned_data['matricula']
            if Publicacion_ObjetoValioso.objects.filter(matricula=matricula).exists():
                messages.error(request, 'Ya existe una publicación con la misma matrícula.')
            else:
                form.save()
                messages.success(request, 'Publicación exitosa')  # Enviar mensaje de éxito
                return redirect('list_publication')  # Redirige a la vista de lista de publicaciones
    else:
        form = PublicacionObjetoValiosoForm(usuario)
    return render(request, 'registrar_publicacion.html', {'form': form})

def registrar_Embarcacion(request):
    usuario = request.session['user_id']
    if request.method == 'POST':
        form = PublicacionEmbarcacionForm(usuario, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Publicación exitosa')  # Enviar mensaje de éxito
            return redirect('list_publication')
    else:
        form = PublicacionEmbarcacionForm(usuario)
    return render(request, 'registrar_publicacion_boat.html', {'form': form})
    return redirect(request.META.get('HTTP_REFERER', '/'))


def finalizar_trueque(request, publicacion_id, tipo_obj):
    if tipo_obj == 'Objetos Valiosos':
        publi = get_object_or_404(Publicacion_ObjetoValioso, id=publicacion_id)
        user = publi.dueño
        solicitud = get_object_or_404(Solicitud_ObjetosValiosos, publicacion_id=publicacion_id)
        interesado_id = solicitud.usuario_interesado_id  # Obtener el ID del usuario interesado
        intere = get_object_or_404(User, id=interesado_id)
    else:
        publi = get_object_or_404(Publicacion_Embarcacion, id=publicacion_id)
        user = publi.embarcacion.dueno
        solicitud = get_object_or_404(Solicitud_Embarcaciones, publicacion_id=publicacion_id)
        interesado_id = solicitud.usuario_interesado_id  # Obtener el ID del usuario interesado
        intere = get_object_or_404(User, id=interesado_id)

    if user.moroso:
        return JsonResponse({'moroso': True})
    if intere.moroso:
        return JsonResponse({'moroso': True})

    subject = 'Trueque finalizado'
    message = f'Hola {intere.nombre}, el trueque de {publi.descripcion} ha finalizado'
    send_mail(subject, message, settings.EMAIL_HOST_USER, [intere.mail])

    subject = 'Trueque finalizado'
    message = f'Hola {user.nombre}, el trueque de {publi.descripcion} ha finalizado'
    send_mail(subject, message, settings.EMAIL_HOST_USER, [user.mail])

    publi.estado = "Finalizado"
    publi.save()
    return JsonResponse({'moroso': False})


@require_POST
def eliminar_mensaje(request, mensaje_id):
    mensaje = Mensajes_chat.objects.get(id=mensaje_id)
    mensaje.delete()
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


def denunciar_usuario(request, sender_id):
    usuario_denunciante = get_object_or_404(User, id=request.session.get('user_id'))

    usuario_denunciado = get_object_or_404(User, id=sender_id)

    if Denuncia.objects.filter(denunciado=usuario_denunciado, denunciante=usuario_denunciante).exists():
        messages.warning(request, 'Usted ya ha denunciado al usuario. El administrador tomará las decisiones pertinentes')
    else:
        # Crear la nueva denuncia
        nueva_denuncia = Denuncia(denunciado=usuario_denunciado, denunciante=usuario_denunciante)
        nueva_denuncia.save()
        messages.success(request, 'Denuncia realizada correctamente.')
        subject = 'Han denunciado un mensaje que enviaste'
        message = f'Hola {usuario_denunciado.nombre}, han denunciado un comentario que hiciste en el mensaje, para mas información contactarte con la administración'
        send_mail(subject, message, settings.EMAIL_HOST_USER, [usuario_denunciado.mail])

    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

