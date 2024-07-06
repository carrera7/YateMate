from django.shortcuts import render, redirect, get_object_or_404
from .forms import ValoracionTruequeForm, ValoracionAmarraForm, RespuestaValoracionForm, RespuestaValoracionAmarraForm
from .models import Valoracion_Trueque, Valoracion_Amarra
from django.contrib import messages
from Register.models import User
from django.urls import reverse

def valoraciones_list_pendientes(request):
    # Obtener el usuario activo
    usuario_id = request.session.get('user_id')
    usuario_tipo = request.session.get('user_type')
    
    # Obtener todas las valoraciones en estado "Inicio" del usuario activo
    valoraciones_trueque = Valoracion_Trueque.objects.filter(estado='Inicio', usuario_id=usuario_id)
    valoraciones_amarra = Valoracion_Amarra.objects.filter(estado='Inicio', usuario_id=usuario_id)

    # Obtener el filtro seleccionado (por defecto 'trueque' si no hay filtro seleccionado)
    filtro = request.GET.get('filtro', 'trueque')

    if filtro == 'trueque':
        valoraciones_trueque = valoraciones_trueque
        valoraciones_amarra = Valoracion_Amarra.objects.none()
    elif filtro == 'amarra':
        valoraciones_trueque = Valoracion_Trueque.objects.none()
        valoraciones_amarra = valoraciones_amarra

    contexto = {
        'valoraciones_trueque': valoraciones_trueque,
        'valoraciones_amarra': valoraciones_amarra,
        'filtro': filtro,
        'usuario_tipo': usuario_tipo,
    }
    return render(request, 'valoraciones_list_pendientes.html', contexto)

def valoraciones_list_realizadas(request):
    # Obtener el usuario activo
    usuario_id = request.session.get('user_id')
    usuario_tipo = request.session.get('user_type')
    
    # Obtener todas las valoraciones en estado "Proceso" del usuario activo
    valoraciones_trueque = Valoracion_Trueque.objects.filter(estado='Proceso', usuario_id=usuario_id)
    valoraciones_amarra = Valoracion_Amarra.objects.filter(estado='Proceso', usuario_id=usuario_id)


    # Obtener el filtro seleccionado (por defecto 'trueque' si no hay filtro seleccionado)
    filtro = request.GET.get('filtro', 'trueque')

    if filtro == 'trueque':
        valoraciones_trueque = valoraciones_trueque
        valoraciones_amarra = Valoracion_Amarra.objects.none()
    elif filtro == 'amarra':
        valoraciones_trueque = Valoracion_Trueque.objects.none()
        valoraciones_amarra = valoraciones_amarra

    contexto = {
        'valoraciones_trueque': valoraciones_trueque,
        'valoraciones_amarra': valoraciones_amarra,
        'filtro': filtro,
        'usuario_tipo': usuario_tipo,
    }
    return render(request, 'valoraciones_list_realizadas.html', contexto)

def valoraciones_list_contestadas(request):
    # Obtener el usuario activo
    usuario_id = request.session.get('user_id')
    usuario_tipo = request.session.get('user_type')
    
    # Obtener todas las valoraciones en estado "Finalizado" del usuario activo
    valoraciones_trueque = Valoracion_Trueque.objects.filter(estado='Finalizado', usuario_id=usuario_id)
    valoraciones_amarra = Valoracion_Amarra.objects.filter(estado='Finalizado', usuario_id=usuario_id)

    # Obtener el filtro seleccionado (por defecto 'trueque' si no hay filtro seleccionado)
    filtro = request.GET.get('filtro', 'trueque')

    if filtro == 'trueque':
        valoraciones_trueque = valoraciones_trueque
        valoraciones_amarra = Valoracion_Amarra.objects.none()
    elif filtro == 'amarra':
        valoraciones_trueque = Valoracion_Trueque.objects.none()
        valoraciones_amarra = valoraciones_amarra

    contexto = {
        'valoraciones_trueque': valoraciones_trueque,
        'valoraciones_amarra': valoraciones_amarra,
        'filtro': filtro,
        'usuario_tipo': usuario_tipo,
    }
    return render(request, 'valoraciones_list_contestadas.html', contexto)

def eliminar_valoracion_trueque(request, valoracion_id):
    if request.method == 'POST':
        valoracion = get_object_or_404(Valoracion_Trueque, id=valoracion_id)
        valoracion.delete()
        messages.success(request, 'Valoración de trueque eliminada.')
        return redirect('valoraciones_list_pendientes')  # Redirige a la lista de valoraciones pendientes
    messages.error(request, 'Método no permitido.')
    return redirect('valoraciones_list_pendientes')

def valorar_trueque(request, id):
    valoracion = get_object_or_404(Valoracion_Trueque, id=id)
    if request.method == 'POST':
        if 'guardar' in request.POST:
            form = ValoracionTruequeForm(request.POST, instance=valoracion)
            if form.is_valid():
                form.save()
                valoracion.estado = 'Proceso'
                valoracion.save()
                return redirect('valoraciones_list_pendientes')
        else:
                form = ValoracionTruequeForm(instance=valoracion)
                return render(request, 'valorar_trueque.html', {'form': form})
    else:
        form = ValoracionTruequeForm(instance=valoracion)
    return render(request, 'valorar_trueque.html', {'form': form})

def eliminar_valoracion_amarra(request, valoracion_id):
    if request.method == 'POST':
        valoracion = get_object_or_404(Valoracion_Amarra, id=valoracion_id)
        valoracion.delete()
        messages.success(request, 'Valoración de amarra eliminada.')
        return redirect('valoraciones_list_pendientes')  # Redirige a la lista de valoraciones pendientes
    messages.error(request, 'Método no permitido.')
    return redirect('valoraciones_list_pendientes')

def valorar_amarra(request, id):
    valoracion = get_object_or_404(Valoracion_Amarra, id=id)
    if request.method == 'POST':
        if 'guardar' in request.POST:
            form = ValoracionAmarraForm(request.POST, instance=valoracion)
            if form.is_valid():
                form.save()
                valoracion.estado = 'Proceso'
                valoracion.save()
                return redirect('valoraciones_list_pendientes')
        else:
            form = ValoracionAmarraForm(instance=valoracion)
            return render(request, 'valorar_Amarra.html', {'form': form})
    else:
        form = ValoracionAmarraForm(instance=valoracion)
    return render(request, 'valorar_Amarra.html', {'form': form})

def mis_valoraciones(request):
    # Obtener el usuario activo
    usuario_id = request.session.get('user_id')
    usuario_tipo = request.session.get('user_type')

    # Obtener el filtro seleccionado (por defecto 'trueque' si no hay filtro seleccionado)
    filtro = request.GET.get('filtro', 'trueque')
    estado_filtro = request.GET.get('estado', 'proceso')

    # Filtrar las valoraciones según el estado y el tipo de usuario
    if estado_filtro == 'proceso':
        valoraciones_trueque = Valoracion_Trueque.objects.filter(estado='Proceso', dueño_id=usuario_id)
        valoraciones_amarra = Valoracion_Amarra.objects.filter(estado='Proceso', dueño_id=usuario_id)
    elif estado_filtro == 'finalizado':
        valoraciones_trueque = Valoracion_Trueque.objects.filter(estado='Finalizado', dueño_id=usuario_id)
        valoraciones_amarra = Valoracion_Amarra.objects.filter(estado='Finalizado', dueño_id=usuario_id)
    else:
        valoraciones_trueque = Valoracion_Trueque.objects.none()
        valoraciones_amarra = Valoracion_Amarra.objects.none()

    # Si el usuario es de tipo "Usuario", no mostrar valoraciones de amarras en proceso
    if usuario_tipo == 'Usuario' and filtro == 'amarra':
        valoraciones_amarra = Valoracion_Amarra.objects.none()

    contexto = {
        'valoraciones_trueque': valoraciones_trueque,
        'valoraciones_amarra': valoraciones_amarra,
        'usuario_tipo': usuario_tipo,
        'filtro': filtro,
        'estado_filtro': estado_filtro,
    }
    return render(request, 'mis_valoraciones.html', contexto)

def responder_valoracion_trueque(request, id):
    valoracion = get_object_or_404(Valoracion_Trueque, id=id)
    if request.method == 'POST':
        form = RespuestaValoracionForm(request.POST, instance=valoracion)
        if form.is_valid():
            valoracion = form.save(commit=False)
            valoracion.estado = 'Finalizado'
            valoracion.save()
            return redirect('mis_valoraciones')
    else:
        form = RespuestaValoracionForm(instance=valoracion)
    return render(request, 'responder_valoracion.html', {'form': form, 'valoracion': valoracion})

def responder_valoracion_amarra(request, id):
    valoracion = get_object_or_404(Valoracion_Amarra, id=id)
    if request.method == 'POST':
        form = RespuestaValoracionAmarraForm(request.POST, instance=valoracion)
        if form.is_valid():
            valoracion = form.save(commit=False)
            valoracion.estado = 'Finalizado'
            valoracion.save()
            return redirect('mis_valoraciones')
    else:
        form = RespuestaValoracionAmarraForm(instance=valoracion)
    return render(request, 'responder_valoracion.html', {'form': form, 'valoracion': valoracion})

def modificar_valoracion_trueque(request, valoracion_id):
    valoracion = get_object_or_404(Valoracion_Trueque, pk=valoracion_id)

    if request.method == 'POST':
        # Procesar el formulario de modificación aquí si es necesario
        # Por ejemplo, actualizar el campo de respuesta y cambiar el estado a 'Finalizado'
        valoracion.respuesta = request.POST.get('respuesta')
        valoracion.estado = 'Finalizado'
        valoracion.save()

        # Redirigir a alguna página de confirmación o lista de valoraciones
        return redirect('mis_valoraciones')  # Ajusta la URL a donde deseas redirigir

    contexto = {
        'valoracion': valoracion,
    }
    return render(request, 'modificar_valoracion_trueque.html', contexto)

def modificar_valoracion_amarra(request, valoracion_id):
    valoracion = get_object_or_404(Valoracion_Amarra, pk=valoracion_id)

    if request.method == 'POST':
        # Procesar el formulario de modificación aquí si es necesario
        # Por ejemplo, actualizar el campo de respuesta y cambiar el estado a 'Finalizado'
        valoracion.respuesta = request.POST.get('respuesta')
        valoracion.estado = 'Finalizado'
        valoracion.save()

        # Redirigir a alguna página de confirmación o lista de valoraciones
        return redirect('mis_valoraciones')  # Ajusta la URL a donde deseas redirigir

    contexto = {
        'valoracion': valoracion,
    }
    return render(request, 'modificar_valoracion_amarra.html', contexto)

def listar_valoraciones_de_usuarios(request):
    # Obtener parámetros de filtrado
    tipo_valoracion = request.GET.get('tipo_valoracion', '')  # Puede ser 'trueque', 'amarra' o vacío (todos)
    usuario_nombre = request.GET.get('usuario_nombre', '')  # Nombre del usuario para buscar

    # Obtener todos los usuarios que tienen al menos una valoración
    usuarios_con_valoraciones = User.objects.filter(
        id__in=Valoracion_Trueque.objects.values_list('usuario_id', flat=True).distinct()) | \
        User.objects.filter(id__in=Valoracion_Amarra.objects.values_list('usuario_id', flat=True).distinct())

    # Filtrar por tipo de valoración si se especifica
    if tipo_valoracion:
        if tipo_valoracion == 'trueque':
            usuarios_con_valoraciones = usuarios_con_valoraciones.filter(id__in=Valoracion_Trueque.objects.values_list('usuario_id', flat=True).distinct())
        elif tipo_valoracion == 'amarra':
            usuarios_con_valoraciones = usuarios_con_valoraciones.filter(id__in=Valoracion_Amarra.objects.values_list('usuario_id', flat=True).distinct())

    # Filtrar por nombre de usuario si se especifica
    if usuario_nombre:
        usuarios_con_valoraciones = usuarios_con_valoraciones.filter(username__icontains=usuario_nombre)

    contexto = {
        'usuarios': usuarios_con_valoraciones,
        'tipo_valoracion': tipo_valoracion,
        'usuario_nombre': usuario_nombre,
    }
    return render(request, 'valoraciones_de_usuarios.html', contexto)

def detalle_valoraciones_usuario(request, usuario_id):
    usuario = get_object_or_404(User, id=usuario_id)
    
    # Obtener todas las valoraciones del usuario
    valoraciones_trueque = Valoracion_Trueque.objects.filter(usuario=usuario)
    valoraciones_amarra = Valoracion_Amarra.objects.filter(usuario=usuario)
    
    contexto = {
        'usuario': usuario,
        'valoraciones_trueque': valoraciones_trueque,
        'valoraciones_amarra': valoraciones_amarra,
    }
    return render(request, 'detalle_valoraciones_usuario.html', contexto)