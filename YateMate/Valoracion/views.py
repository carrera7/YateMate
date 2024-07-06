from django.shortcuts import render, redirect, get_object_or_404
from .forms import ValoracionTruequeForm, ValoracionAmarraForm
from .models import Valoracion_Trueque, Valoracion_Amarra
from django.contrib import messages
from django.urls import reverse

def valoraciones_list_pendientes(request):
    # Obtener el usuario activo
    usuario_id = request.session.get('user_id')
    
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
    }
    return render(request, 'valoraciones_list_pendientes.html', contexto)

def valoraciones_list_realizadas(request):
    usuario_id = request.session.get('user_id')
    
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
    }
    return render(request, 'valoraciones_list_realizadas.html', contexto)

def valoraciones_list_contestadas(request):
    usuario_id = request.session.get('user_id')
    
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
