from django.contrib import messages
from django.shortcuts import render, redirect,get_object_or_404
from Register.models import User
from django.core.mail import send_mail
from django.core.exceptions import PermissionDenied



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
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Usuario registrado correctamente.")
            return redirect('index')  # Redirige a la página de inicio de sesión después del registro
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