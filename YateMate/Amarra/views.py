from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms import AmarraForm
from django.contrib import messages
from .models import Publicacion_Amarra
from Register.models import User
from datetime import datetime, timedelta

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


def ver_Reservas (request):
    user_id = request.session['user_id']
    reservas= Publicacion_Amarra.objects.filter(dueño=user_id)
    return render (request, "ver_mis_reservas.html",{'objetos': reservas})
