from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.shortcuts import render, redirect
from .forms import AmarraForm
from django.contrib import messages
from .models import Publicacion_Amarra , Reserva
from Register.models import User
from datetime import datetime, timedelta, timezone

def list_amarra(request):
    if request.method == 'GET' and 'fecha_inicio' in request.GET:
        fecha_inicio = request.GET.get('fecha_inicio')
        try:
            fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, 'Formato de fecha inválido.')
            return redirect('list_amarra')
        
        Amarras = Publicacion_Amarra.objects.filter(
            fecha_inicio__gte=fecha_inicio
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
    cant_dias = int(publicacion.cant_dias) - 1 
    fecha_fin = fecha_inicio + timedelta(days=cant_dias)
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
        fechas_seleccionadas = [datetime.strptime(fecha, '%Y-%m-%d') for fecha in fechas_seleccionadas]
        fechas_seleccionadas.sort()

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

        return redirect('list_amarra')  # Redirigir a una página de confirmación o donde prefieras

    context = {
        'fechas_disponibles': fechas_disponibles_str,
    }
    return render(request, 'crear_reserva.html', context)

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
    
    reserva.fecha_salida =  datetime.now().date()
    
    # Acceder a la publicación asociada
    publicacion = reserva.publicacion
    
    # Obtengo la fecha de la publicación y aseguro que sea un objeto date
    publicacion_fecha_creacion = publicacion.fecha_inicio
    if isinstance(publicacion_fecha_creacion, datetime):
        publicacion_fecha_creacion = publicacion_fecha_creacion.date()
    
    # Obtengo la fecha de ingreso de la reserva y aseguro que sea un objeto date
    reserva_fecha_ingreso = reserva.fecha_salida
    if isinstance(reserva_fecha_ingreso, datetime):
        reserva_fecha_ingreso = reserva_fecha_ingreso.date()
    
    # Calcula la diferencia de tiempo entre la fecha de creación y la fecha de ingreso
    diferencia_tiempo = reserva_fecha_ingreso - publicacion_fecha_creacion
    
    # Verificar el tipo de diferencia_tiempo
    if isinstance(diferencia_tiempo, timedelta):
        # Obtiene la cantidad de días de la diferencia de tiempo
        cantidad_dias = diferencia_tiempo.days
    
    if (int(publicacion.cant_dias) - cantidad_dias) == 0:
        publicacion.estado = 'Finalizado'
    else:
        publicacion.cant_dias = int(publicacion.cant_dias) - cantidad_dias
        publicacion.fecha_inicio = datetime.now().date()
        publicacion.estado = 'Vigente'
        publicacion.save()
        
    reserva.fecha_salida =  datetime.now().date()
    reserva.save()
    return redirect('reservas')
