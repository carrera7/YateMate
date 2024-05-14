from django.contrib import messages
from django.shortcuts import render, redirect,get_object_or_404
from Register.models import User
from django.core.mail import send_mail

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
                return render(request, 'login.html', {'error_message': 'Credenciales inválidas'})
        except User.DoesNotExist:
            # Mostrar un mensaje de error si el usuario no existe
            return render(request, 'login.html', {'error_message': 'El usuario no existe'})
    else:
        return render(request, 'login.html')
    
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
            messages.success(request, "Usuario registrado correctamente. Se le enviara un mail cuando su usuario este activo.")
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
    usuario = get_object_or_404(User, pk=usuario_id)
    usuario.tipo = 'Cliente'
    usuario.save()

    # Envío de correo electrónico al usuario
    subject = '¡Tu cuenta ha sido habilitada!'
    message = 'Hola {},\n\nTu cuenta en nuestra plataforma ha sido habilitada como Cliente. ¡Bienvenido de nuevo!\n\nAtentamente,\nEl equipo de YateMate'.format(usuario.mail)
    from_email = 'digitalinnovation09@gmail.com'  # Cambia esto por tu dirección de correo
    to_email = usuario.mail
    send_mail(subject, message, from_email, [to_email])

    usuarios_inhabilitados = User.objects.filter(tipo='Usuario')
    context = {
        'usuarios_inhabilitados': usuarios_inhabilitados
    }
    return render(request, 'enable_accounts.html', context)