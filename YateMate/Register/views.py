from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import EmbarcacionForm

def crear_embarcacion(request):
    if request.method == 'POST':
        form = EmbarcacionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Embarcación registrada con éxito.')
            return redirect('index')
    else:
        form = EmbarcacionForm()
    return render(request, 'register_Boat.html', {'form': form})