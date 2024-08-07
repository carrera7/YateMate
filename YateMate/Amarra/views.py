from django.shortcuts import get_object_or_404, render
from django.shortcuts import render, redirect
from .forms import AmarraForm , ModificarPublicacionForm
from django.contrib import messages
from .models import Publicacion_Amarra , Reserva
from Register.models import User
from django.utils import timezone
from datetime import datetime, timedelta
from django.db import transaction
from Valoracion.models import Valoracion_Amarra, Mensaje
from decimal import Decimal




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
    if Reserva.objects.filter(publicacion=publicacion, estado__in=['Vigente', 'En Proceso']).exists():
        messages.success(request, "Esta operación no es posible, existe una reserva") 
        return redirect ('mis_publicaciones')
    else:    
        publicacion.delete()
        messages.success(request, 'Publicacion eliminada')
    return redirect('mis_publicaciones')

def modificar_publicacion(request, id):
    publicacion = get_object_or_404(Publicacion_Amarra, id=id)
    
    if request.method == 'POST':
        form = ModificarPublicacionForm(request.POST)
        if form.is_valid():
            dias_a_agregar = form.cleaned_data['dias_a_agregar']
            nuevo_precio = form.cleaned_data['nuevo_precio']
            
            publicacion.cant_dias = str(int(publicacion.cant_dias) + dias_a_agregar)
            publicacion.precio = str(Decimal(publicacion.precio) + Decimal(nuevo_precio))
            publicacion.actualizar_dias_disponibles()
            publicacion.save()
            
            messages.success(request, 'Publicación modificada exitosamente.')
            return redirect('mis_publicaciones')  # Cambia esto por la URL correcta
    else:
        form = ModificarPublicacionForm(initial={'nuevo_precio': publicacion.precio})
    
    return render(request, 'modificar_publicacion.html', {'publicacion': publicacion, 'form': form})

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
        
        # Obtener todas las fechas reservadas por el usuario en otras publicaciones
        reservas_usuario = Reserva.objects.filter(usuario=usuario).exclude(publicacion=publicacion)
        fechas_reservadas_usuario = set()
        for reserva in reservas_usuario:
            fecha_ingreso = reserva.fecha_ingreso
            cant_dias = int(reserva.cant_dias)
            if (cant_dias == 1):
                fechas_reservadas_usuario.add(fecha_ingreso)
            else:    
                for i in range(cant_dias):
                    fechas_reservadas_usuario.add(fecha_ingreso + timedelta(days=i))

        # Verificar si hay solapamiento de fechas con las reservas existentes del usuario
        for fecha in fechas_seleccionadas:
            if fecha in fechas_reservadas_usuario:
                messages.error(request, 'Usted tiene una reserva en la cual se solapan las fechas.')
                return redirect('list_amarra')

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
            messages.error(request, "Publicación fallida por ser moroso")
            return redirect('list_amarra')
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
    
    # Verificar si ya existe una valoración de amarra para esta reserva y usuario
    valoracion_existente = Valoracion_Amarra.objects.filter(
        publicacion_amarra=reserva.publicacion,
        usuario=reserva.usuario
    ).exists()
    
    if not valoracion_existente:
        # Crear una valoración de amarra
        valoracion = Valoracion_Amarra(
            publicacion_amarra=reserva.publicacion,
            usuario=reserva.usuario,
            estrellas=0,  # Se puede ajustar según sea necesario
            comentario='',  # Se puede ajustar según sea necesario
            estado='Inicio'
        )
        valoracion.save()
        
        mensaje = Mensaje(
            usuario=reserva.usuario,
            valoracion_amarra=valoracion,
            estado='Pendiente',
            mensaje_texto="Usted tiene una valoración pendiente de una amarra",
            mostrar=True
        )
        mensaje.save()
    
    #agregar notificacion 
    
    return redirect('reservas') 

def mis_reservas(request):
    usuario_id = request.session.get('user_id')
    reservas = Reserva.objects.filter(usuario=usuario_id, estado='Vigente')
    return render(request, 'mis_reservas.html', {'reservas': reservas})

def eliminar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    # Actualiza la cantidad de días disponibles de la publicación
    publicacion = reserva.publicacion
    publicacion.cant_dias_disponibles = str(int(publicacion.cant_dias_disponibles) + int(reserva.cant_dias))
    
    # Vuelve a guardar la publicación para reflejar los cambios
    publicacion.save()
    
    # Elimina la reserva
    reserva.delete()
    return redirect("Ver_mis_reservas")