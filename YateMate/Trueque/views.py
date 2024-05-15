from django.shortcuts import render
from Register.models import User
from .models import Publicacion_ObjetoValioso, Publicacion_Embarcacion , Solicitud_Embarcaciones , Solicitud_ObjetosValiosos
from Register.models import Embarcacion
from itertools import chain



def list_publication(request):
    embarcaciones_vigentes = Publicacion_Embarcacion.objects.filter(estado='Vigente')
    objetos_vigentes = Publicacion_ObjetoValioso.objects.filter(estado='Vigente')
    
    tipo_filtro = request.GET.get('tipo', 'objetos valiosos')  # Valor por defecto 'objetos valiosos'
    
    if tipo_filtro == 'objetos valiosos':
        objetos = objetos_vigentes
    elif tipo_filtro == 'embarcaciones':
        objetos = embarcaciones_vigentes
        
    tipo_objetos = 'Objetos Valiosos' if tipo_filtro == 'objetos valiosos' else 'Embarcaciones'
    
    return render(request, "list_publication.html", {'objetos': objetos , 'tipo_objetos': tipo_objetos,})

# se necesita autenticarse
def list_publication_boat(request):
    embarcaciones_vigentes = Publicacion_Embarcacion.objects.filter(estado='Vigente')
    return render(request, "list_publication_boat.html", {'embarcaciones_vigentes': embarcaciones_vigentes,'tipo_objetos': 'Embarcaciones',})

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

    # Agregar el tipo al contexto para pasarlo al HTML
    tipo_objetos = 'Objetos Valiosos' if tipo_filtro == 'objetos valiosos' else 'Embarcaciones'

    # Renderizar el HTML con los datos filtrados o no
    return render(request, 'list.html', {
        'objetos': objetos,
        'tipo_objetos': tipo_objetos,
    })
    
def mis_publicaciones(request):
    
    objetos = Publicacion_ObjetoValioso.objects.filter(dueño=request.session['user_id'])
    embarcaciones = Publicacion_Embarcacion.objects.filter(embarcacion__dueno_id=request.session['user_id'])

    return render(request, "ver_mis_publicaciones.html",{'objetos': objetos, 'embarcaciones': embarcaciones})
 
def solicitudes_trueque(request):
    return render(request, "ver_solicitudes_trueque.html") 
 
def solicitud_embarcacion(request, publicacion_id):
    user_id = request.session['user_id']
    user = User.objects.get(id=user_id)
    publicacion = Publicacion_Embarcacion.objects.get(id=publicacion_id)
    
    if Solicitud_Embarcaciones.objects.filter(publicacion=publicacion, usuarios_interesados=user).exists():
            mensaje = 'Ya tienes una solicitud previa de esta publicación.'
    else:
        solicitud = Solicitud_Embarcaciones.objects.create(publicacion=publicacion)
        solicitud.usuarios_interesados.add(user)
        solicitud.save()
        mensaje = 'La solicitud fue exitosa.'
    
    return render(request, 'ver_mas.html', {'objeto': publicacion, 'tipo_objetos':'Embarcaciones', 'mensaje':mensaje })
    
def solicitud_objeto_valioso(request, publicacion_id):
    user_id = request.session['user_id']
    user = User.objects.get(id=user_id)
    publicacion = Publicacion_ObjetoValioso.objects.get(id=publicacion_id)
    # Verificar si el usuario ya tiene una solicitud previa de esta publicación
    if Solicitud_ObjetosValiosos.objects.filter(publicacion=publicacion, usuarios_interesados=user).exists():
        mensaje = 'Ya tienes una solicitud previa de esta publicación.'
    else:
        solicitud = Solicitud_ObjetosValiosos.objects.create(publicacion=publicacion)
        solicitud.usuarios_interesados.add(user)
        solicitud.save()
        mensaje = 'La solicitud fue exitosa.'


    return render(request, 'ver_mas.html', {'objeto': publicacion, 'tipo_objetos': 'Objetos Valiosos' , 'mensaje': mensaje})
 
def saber_mas(request, id, tipo_objetos):
    # Dependiendo del tipo de objeto, obtén la publicación correspondiente
    if tipo_objetos == 'Objetos Valiosos':
        objeto = Publicacion_ObjetoValioso.objects.get(id=id)
    elif tipo_objetos == 'Embarcaciones':
        objeto = Publicacion_Embarcacion.objects.get(id=id)
    else:
        # Manejar el caso en el que el tipo de objeto no sea válido
        return render(request, 'error.html', {'mensaje': 'Tipo de objeto no válido'})

    return render(request, 'ver_mas.html', {'objeto': objeto, 'tipo_objetos': tipo_objetos})

def eliminarObjeto(request, id):
    # logica para eliminar las solicitudes
    
    # Elimino el Objeto
    objeto = Publicacion_ObjetoValioso.objects.get(id=id)
    objeto.delete()
    
    objetos = Publicacion_ObjetoValioso.objects.filter(dueño=request.session['user_id'])
    embarcaciones = Publicacion_Embarcacion.objects.filter(embarcacion__dueno_id=request.session['user_id'])
    
    return render(request, "ver_mis_publicaciones.html",{'objetos': objetos, 'embarcaciones': embarcaciones})

def eliminarEmbarcacion(request, id):
    # logica para eliminar las solicitdes
    
    # Elimino embarcacion
    objeto = Publicacion_Embarcacion.objects.get(id=id)
    objeto.delete()
    
    objetos = Publicacion_ObjetoValioso.objects.filter(dueño=request.session['user_id'])
    embarcaciones = Publicacion_Embarcacion.objects.filter(embarcacion__dueno_id=request.session['user_id'])
    
    return render(request, "ver_mis_publicaciones.html",{'objetos': objetos, 'embarcaciones': embarcaciones})


