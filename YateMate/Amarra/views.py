from django.shortcuts import get_object_or_404, render
from django.shortcuts import render, redirect
from .forms import AmarraForm
from django.contrib import messages
from .models import Publicacion_Amarra , Reserva
from Register.models import User
from django.utils import timezone
from datetime import datetime, timedelta
from django.db import transaction




def list_amarra(request):
    if request.method == 'GET' and 'fecha_inicio' in request.GET:
        fecha_inicio = request.GET.get('fecha_inicio')
        try:
            fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
            if fecha_inicio < timezone.now().date():
                messages.error(request, 'La fecha no puede ser en el pasado.')
                return redirect('list_amarra')
        except ValueError:
            messages.error(request, 'Formato de fecha inválido.')
            return redirect('list_amarra')
        
        Amarras = Publicacion_Amarra.objects.filter(fecha_inicio__lte=fecha_inicio)
        Amarras = [amarra for amarra in Amarras if amarra.is_available_on(fecha_inicio)]
    else:
        usuario_id = request.session.get('user_id')
        if usuario_id:
            usuario = get_object_or_404(User, id=usuario_id)
            Amarras = Publicacion_Amarra.objects.exclude(dueño=usuario)
        else:
            Amarras = Publicacion_Amarra.objects.all()

        # Filtrar las publicaciones que tienen días disponibles
        Amarras = [amarra for amarra in Amarras if int(amarra.cant_dias_disponibles) > 0]

    # Actualizar la cantidad de días disponibles
    for amarra in Amarras:
        amarra.actualizar_dias_disponibles()

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
    if Reserva.objects.filter(publicacion=publicacion).exists:
        messages.success(request, "Esta operación no es posible, existe una reserva") 
        return redirect ('mis_publicaciones')
    else:    
        publicacion.delete()
        messages.success(request, 'Publicacion eliminada')
    return redirect('list_amarra')

def modificar_publicacion(request, id):
    publicacion = get_object_or_404(Publicacion_Amarra, id=id)
    # Lógica para modificar la publicación
    # ...
    return render(request, 'modificar_publicacion.html', {'publicacion': publicacion})

def ver_reservas(request, id):
    publicacion = get_object_or_404(Publicacion_Amarra, id=id)
    reservas = Reserva.objects.filter(publicacion=publicacion).order_by('fecha_ingreso')
    return render(request, 'ver_reservas.html', {'publicacion': publicacion, 'reservas': reservas})

def son_fechas_consecutivas(fechas):
    # Función para verificar si las fechas son consecutivas
    fechas = [datetime.strptime(fecha, '%Y-%m-%d') for fecha in fechas]
    fechas.sort()
    for i in range(1, len(fechas)):
        if (fechas[i] - fechas[i-1]).days != 1:
            return False
    return True

def crear_reserva(request, publicacion_id):
    publicacion = get_object_or_404(Publicacion_Amarra, id=publicacion_id)
    fecha_inicio = publicacion.fecha_inicio
    cant_dias = int(float(publicacion.cant_dias))
    fecha_fin = fecha_inicio + timedelta(days=cant_dias - 1)
    usuario = get_object_or_404(User, id=request.session['user_id'])

    # Generar listado de fechas disponibles
    fechas_disponibles = []
    fecha_actual = fecha_inicio
    while fecha_actual <= fecha_fin:
        fechas_disponibles.append(fecha_actual)
        fecha_actual += timedelta(days=1)

    # Excluir fechas ya reservadas
    reservas = Reserva.objects.filter(publicacion=publicacion)
    fechas_reservadas = set()
    for reserva in reservas:
        fecha_ingreso = reserva.fecha_ingreso
        cant_dias = int(reserva.cant_dias)
        for i in range(cant_dias):
            fechas_reservadas.add(fecha_ingreso + timedelta(days=i))

    # Excluir fechas pasadas
    hoy = datetime.now().date()
    fechas_disponibles = [fecha for fecha in fechas_disponibles if fecha >= hoy]

    # Excluir fechas ya reservadas
    fechas_disponibles = [fecha for fecha in fechas_disponibles if fecha not in fechas_reservadas]
    fechas_disponibles_str = [fecha.strftime('%Y-%m-%d') for fecha in fechas_disponibles]

    if request.method == 'POST':
        fechas_seleccionadas = request.POST.getlist('fechas_seleccionadas')
        fechas_seleccionadas = [datetime.strptime(fecha, '%Y-%m-%d').date() for fecha in fechas_seleccionadas]
        fechas_seleccionadas.sort()

        with transaction.atomic():
            if not son_fechas_consecutivas([fecha.strftime('%Y-%m-%d') for fecha in fechas_seleccionadas]):
                # Crear una reserva para cada fecha seleccionada
                for fecha in fechas_seleccionadas:
                    reserva = Reserva(
                        publicacion=publicacion,
                        fecha_ingreso=fecha,
                        cant_dias='1',
                        usuario=usuario
                    )
                    reserva.save()
            else:
                # Crear una única reserva con las fechas consecutivas
                fecha_ingreso = min(fechas_seleccionadas)
                cant_dias = len(fechas_seleccionadas)

                reserva = Reserva(
                    publicacion=publicacion,
                    fecha_ingreso=fecha_ingreso,
                    cant_dias=str(cant_dias),
                    usuario=usuario
                )
                reserva.save()
        
        messages.success(request, '¡Reserva realizada con éxito!')
        return redirect('list_amarra')

    context = {
        'fechas_disponibles': fechas_disponibles_str,
    }
    return render(request, 'crear_reserva.html', context)

def publicar_Alquiler(request):
    usuario_id = request.session.get('user_id')
    user = User.objects.get(id=usuario_id)
    if request.method == 'POST':
        form = AmarraForm(user,request.POST, request.FILES)
        if form.is_valid():
           if user.moroso:
            messages.success(request, "Publicación fallida por ser moroso")
           else:
                form.save()
                messages.success(request, 'Publicación de alquiler registrada con éxito.')
                return redirect('list_amarra')
    else:
        form = AmarraForm(user)
    return render(request, 'amarra.html', {'form': form})

def reservas(request):
    reservas_finalizadas = Reserva.objects.all()
    return render(request, "reservas.html", {'reservas': reservas_finalizadas})

def registrar_ingreso(request, id):
    reserva = get_object_or_404(Reserva, id=id)
    # Lógica para registrar ingreso
    reserva.estado = 'En Proceso'  # Cambia el estado a "En Proceso"
    reserva.save()
    return redirect('reservas')

def registrar_salida(request, id):
    reserva = get_object_or_404(Reserva, id=id)
    # Lógica para registrar ingreso
    reserva.estado = 'Finalizado'  # Cambia el estado a "En Proceso"
    reserva.save()
    return redirect('reservas') 
