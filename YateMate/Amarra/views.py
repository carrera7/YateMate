from django.shortcuts import get_object_or_404, render
from django.shortcuts import render, redirect
from .forms import AmarraForm
from django.contrib import messages
from .models import Publicacion_Amarra , Reserva
from Register.models import User
from datetime import datetime, timedelta, timezone

def list_amarra(request):
    if request.method == 'GET' and 'fecha_inicio' in request.GET and 'fecha_fin' in request.GET:
        fecha_inicio = request.GET.get('fecha_inicio')
        fecha_fin = request.GET.get('fecha_fin')
        try:
            fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
            fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, 'Formato de fecha inválido.')
            return redirect('list_amarra')
        
        # Calcular la fecha de fin sumando la cantidad de días a la fecha de inicio
        dias = (fecha_fin - fecha_inicio).days
        Amarras = Publicacion_Amarra.objects.filter(
            fecha_inicio__gte=fecha_inicio,
            fecha_inicio__lte=fecha_inicio + timedelta(days=dias)
        )
    else:
        Amarras = Publicacion_Amarra.objects.all()

    return render(request, "list_amarra.html", {'objetos': Amarras})

def mis_publicaciones(request):
    user_id = request.session.get('user_id')
    publicaciones_amarras = Publicacion_Amarra.objects.filter(dueño_id=user_id)

    for publicacion in publicaciones_amarras:
        # Verificar si hay reservas asociadas a esta publicación
        tiene_reservas = Reserva.objects.filter(publicacion=publicacion).exists()
        publicacion.tiene_reservas = tiene_reservas  # Agregar el atributo a la instancia

    return render(request, 'mis_publicaciones.html', {'publicaciones_amarras': publicaciones_amarras})

def eliminar_publicacion(request, id):
    publicacion = get_object_or_404(Publicacion_Amarra, id=id)
    publicacion.delete()
    return redirect('mis_publicaciones')

def modificar_publicacion(request, id):
    publicacion = get_object_or_404(Publicacion_Amarra, id=id)
    # Lógica para modificar la publicación
    # ...
    return render(request, 'modificar_publicacion.html', {'publicacion': publicacion})

def ver_reservas(request, id):
    publicacion = get_object_or_404(Publicacion_Amarra, id=id)
    reservas = Reserva.objects.filter(publicacion=publicacion).order_by('fecha_ingreso', 'fecha_salida')
    return render(request, 'ver_reservas.html', {'publicacion': publicacion, 'reservas': reservas})

def crear_reserva(request, publicacion_id):
    publicacion = get_object_or_404(Publicacion_Amarra, id=publicacion_id)
    usuario = get_object_or_404(User, id=request.session['user_id'])

    # Crear la reserva
    Reserva.objects.create(
        publicacion=publicacion,
        usuario=usuario,
        fecha_ingreso=None,
        fecha_salida=None
    )

    # Actualizar el estado de la publicación a "En Proceso"
    publicacion.estado = 'En Proceso'
    publicacion.save()

    return redirect('list_amarra')  # Redirigir a la vista de reservas del usuario

def publicar_Alquiler(request):
    usuario = User.objects.get(id=request.session['user_id'])  # Asegúrate de que el usuario esté autenticado
    if request.method == 'POST':
        form = AmarraForm(usuario,request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Publicacion de alquiler registrada con éxito.')
            return redirect('list_amarra.html')
    else:
        form = AmarraForm(usuario)
    return render(request, 'amarra.html', {'form': form})

def reservas(request):
    reservas_finalizadas = Reserva.objects.all()
    return render(request, "reservas.html", {'reservas': reservas_finalizadas})

def registrar_ingreso(request, id):
    reserva = get_object_or_404(Reserva, id=id)
    # Lógica para registrar ingreso
    reserva.fecha_ingreso = datetime.now()
    reserva.save()
    return redirect('reservas')

def registrar_salida(request, id):
    reserva = get_object_or_404(Reserva, id=id)
    # Lógica para registrar salida
    reserva.estado = 'Finalizado'
    reserva.save()
    return redirect('reservas')
