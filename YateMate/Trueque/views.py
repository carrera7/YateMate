from django.shortcuts import render
from .models import Publicacion_ObjetoValioso

def list_publication(request):
    objetos_vigentes = Publicacion_ObjetoValioso.objects.filter(estado='Vigente')
    return render(request, "list_publication.html", {'objetos_vigentes': objetos_vigentes})
