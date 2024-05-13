from django.contrib import messages
from django.shortcuts import render, redirect
from Register.models import User
from .froms import CustomUserRegistrationForm

def index(request):
     return render(request, "index.html")

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            # Consultar el usuario en la base de datos
            user = User.objects.get(username=username)
            
            # Verificar si la cuenta está habilitada
            if user.estado_cuenta == 'Habilitado':
                # Verificar si la contraseña coincide
                if password == user.password:
                    # Iniciar sesión en la sesión actual
                    request.session['user_id'] = user.id
                    request.session['user_type'] = user.tipo
                    return redirect('index')  # Redirige a la página principal después del inicio de sesión exitoso
                else:
                    # Mostrar un mensaje de error
                    return render(request, 'login.html', {'error_message': 'Credenciales inválidas'})
            else:
                # Mostrar un mensaje de error si la cuenta no está habilitada
                return render(request, 'login.html', {'error_message': 'La cuenta no está habilitada'})
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