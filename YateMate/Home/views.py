from django.contrib import messages
from django.shortcuts import render, redirect,get_object_or_404
from Register.models import User
from django.core.mail import send_mail
from django.core.exceptions import PermissionDenied
from Trueque.models import Publicacion_Embarcacion, Publicacion_ObjetoValioso
from Amarra.models import Reserva, Publicacion_Amarra
from django.shortcuts import get_object_or_404
from .froms import CustomUserRegistrationForm

def index(request):
     return render(request, "index.html")

def login_view(request):
    if request.method == 'POST':
        mail = request.POST['mail']
        password = request.POST['password']

        try:
            # Consultar el usuario en la base de datos
            user = User.objects.get(mail=mail)
            # Verificar si la contraseña coincide
            if password == user.password:
                # Iniciar sesión en la sesión actual
                request.session['user_id'] = user.id
                request.session['user_type'] = user.tipo
                return redirect('index')  # Redirige a la página principal después del inicio de sesión exitoso
            else:
                # Mostrar un mensaje de error
                return render(request, 'login.html', {'error_message': 'Nombre de usuario o contraseña incorrectos'})
        except User.DoesNotExist:
            # Mostrar un mensaje de error si el usuario no existe
            return render(request, 'login.html', {'error_message': 'Nombre de usuario o contraseña incorrectos'})
    else:
        return render(request, 'login.html',)
    
def logout_view(request):
    if 'user_id' in request.session:
        del request.session['user_id']
        del request.session['user_type']
    return redirect('index')

def register(request):
    if request.GET.get('action') == 'usuario_no_registrado_pu':
        messages.info(request, 'Para hacer una publicación debes estar registrado.')
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # No guardamos todavía para poder modificar el usuario
            user.tipo = 'Usuario'  # Asignamos el tipo de usuario
            user.save()  # Ahora guardamos el usuario con el tipo asignado
            messages.success(request, "Usuario registrado correctamente.")
            return redirect('index')  # Redirige a la página de inicio después del registro
    else:
        form = CustomUserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def usuarios_inhabilitados(request):
    # Obtener todos los usuarios con estado de cuenta "Deshabilitado"
    usuarios_inhabilitados = User.objects.filter(tipo='Usuario')

    # Puedes pasar los usuarios a tu plantilla o hacer cualquier otro procesamiento aquí
    context = {
        'usuarios_inhabilitados': usuarios_inhabilitados
    }

    return render(request, 'enable_accounts.html', context)

def habilitar_usuario(request, usuario_id):
    # Obtener el usuario o devolver un error 404 si no existe
    usuario = get_object_or_404(User, pk=usuario_id)
    
    # Cambiar el tipo de usuario a 'Cliente' y guardar los cambios
    usuario.tipo = 'Cliente'
    usuario.save()

    # Enviar correo electrónico al usuario
    subject = '¡Tu cuenta ha sido habilitada!'
    message = f'Hola {usuario.mail},\n\nTu cuenta en nuestra plataforma ha sido habilitada como Cliente. ¡Bienvenido de nuevo!\n\nAtentamente,\nEl equipo de YateMate'
    from_email = 'yatemate835@gmail.com'  # Cambiar por tu dirección de correo
    to_email = usuario.mail
    send_mail(subject, message, from_email, [to_email])

    # Obtener la lista de usuarios inhabilitados para mostrar en la plantilla
    usuarios_inhabilitados = User.objects.filter(tipo='Usuario')

    # Renderizar la plantilla con la lista actualizada de usuarios inhabilitados
    context = {
        'usuarios_inhabilitados': usuarios_inhabilitados
    }
    return render(request, 'enable_accounts.html', context)

def listado_clientes(request):
    clientes = User.objects.filter(tipo='Cliente')  # Cambiar 'Clientes' por 'Cliente'
    return render(request, "listado_clientes.html", {'clientes': clientes})


def moroso_clientes(request, cliente_id):
    cliente = User.objects.get(id=cliente_id)
    cliente.moroso = True
    cliente.save()
    respuesta = listado_clientes(request)
    return respuesta

def cancelar_deuda(request, cliente_id):
    cliente = User.objects.get(id=cliente_id)
    cliente.moroso = False
    cliente.save()
    respuesta = listado_clientes(request)
    return respuesta

def eliminar_cuenta(request,cliente_id):
    cliente = get_object_or_404(User, id=cliente_id)
    amarra= Publicacion_Amarra.objects.filter(dueño=cliente)
    objetos = Publicacion_ObjetoValioso.objects.filter(dueño=cliente_id)
    embarcaciones = Publicacion_Embarcacion.objects.filter(embarcacion__dueno_id=cliente_id)
    reserva=Reserva.objects.filter(usuario=cliente)
    if not objetos and not embarcaciones and not amarra and not reserva:
        mensaje= 'Baja Exitosa'
        #mostrar el popup y confirmar operacion
        cliente.delete()
        
    else:
        mensaje='Operacion fallida, el usuario tiene operaciones pendientes'

    clientes = User.objects.filter(tipo='Cliente')
    return render(request, "listado_clientes.html", {'clientes': clientes, 'messages':mensaje})
        

