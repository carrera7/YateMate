from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms import AmarraForm
from django.contrib import messages
from .models import Publicacion_Amarra
from Register.models import User

def list_amarra(request):
    #obtengo todos los alquileres 
    #sino   
    Amarras = Publicacion_Amarra.objects.filter()        
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
