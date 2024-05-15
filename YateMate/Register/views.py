from django.shortcuts import render, redirect
from .forms import EmbarcacionForm

def crear_embarcacion(request):
    if request.method == 'POST':
        form = EmbarcacionForm(request.POST, request.FILES)
        if form.is_valid():
            embarcacion = form.save()
            # Hacer algo con la embarcacion creada, como redirigir a una página de detalle
            return redirect('index')
    else:
        form = EmbarcacionForm()
    return render(request, 'register_Boat.html', {'form': form})