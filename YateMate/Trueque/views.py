from django.shortcuts import render
from .models import Publicacion_ObjetoValioso , Publicacion_Embarcacion

def list_publication(request):
    objetos_vigentes = Publicacion_ObjetoValioso.objects.filter(estado='Vigente')
    return render(request, "list_publication.html", {'objetos_vigentes': objetos_vigentes})

# se necesita autenticarse
def list_publication_boat(request):
    embarcaciones_vigentes = Publicacion_Embarcacion.objects.filter(estado='Vigente')
    return render(request, "list_publication_boat.html", {'embarcaciones_vigentes': embarcaciones_vigentes})

def list(request):
    objetos_valiosos = Publicacion_ObjetoValioso.objects.all()
    embarcaciones = Publicacion_Embarcacion.objects.all()

    # Obtener el filtro de tipo y estado de la solicitud GET
    tipo_filtro = request.GET.get('tipo','objetos valiosos')  # Valor por defecto 'objetos valiosos'
    estado_filtro = request.GET.get('estado','Vigente')  # Valor por defecto 'Vigente'

    if tipo_filtro == " ":
        tipo_filtro = 'objetos valiosos'
    if estado_filtro == " ":
          estado_filtro = 'Vigente'   
            
    # Filtrar objetos_valiosos y embarcaciones según el tipo y estado seleccionados
    if tipo_filtro == 'objetos valiosos':
        objetos = objetos_valiosos.filter(estado=estado_filtro)
    elif tipo_filtro == 'embarcaciones':
        objetos = embarcaciones.filter(estado=estado_filtro)

    # Renderizar el HTML con los datos filtrados o no
    return render(request, 'list.html', {
        'objetos': objetos
    })