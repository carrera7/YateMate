from datetime import date
import re 
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator, MinLengthValidator, RegexValidator
import dns
import dns.resolver
from Register.models import User

class CustomUserRegistrationForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ['mail', 'password', 'nombre', 'apellido', 'dni', 'fecha_nacimiento', 'fecha_expiracion_dni', 'nacionalidad', 'genero', 'domicilio', 'cuil_cuit']
        labels = {
            'nombre': 'Nombre',
            'apellido': 'Apellido',
            'dni': 'DNI',
            'fecha_nacimiento': 'Fecha de Nacimiento',
            'fecha_expiracion_dni': 'Fecha de Expiración DNI',
            'nacionalidad': 'Nacionalidad',
            'genero': 'Género',
            'domicilio': 'Domicilio',
            'cuil_cuit': 'CUIL/CUIT',
            'mail': 'Correo Electrónico',
            'tipo': 'Tipo',
        }
        help_texts = {
            'dni': 'El DNI debe contener entre 7 y 8 dígitos numéricos.',
            'cuil_cuit': 'El CUIL/CUIT debe contener entre 11 y 13 caracteres numéricos y guiones.',
            'fecha_nacimiento': 'Formato: DD-MM-AAAA. Ejemplo: 01/02/1990',
            'password': 'La contraseña debe contener al menos una letra mayúscula, una letra minúscula, un número y un carácter especial de la lista @$!%*?&. Ejemplo: P@ssw0rd!',
        }
        error_messages = {
            'dni': {
                'min_length': 'El DNI debe contener al menos 7 caracteres.',
                'max_length': 'El DNI no puede contener más de 8 caracteres.',
                'invalid': 'El DNI solo puede contener números.',
            },
            'cuil_cuit': {
                'min_length': 'El CUIL/CUIT debe contener al menos 11 caracteres.',
                'max_length': 'El CUIL/CUIT no puede contener más de 13 caracteres.',
                'invalid': 'El CUIL/CUIT solo puede contener números y guiones.',
            },
        }
       
    password = forms.CharField(
    label='Contraseña',
    widget=forms.PasswordInput,
    validators=[
        MinLengthValidator(8),
        # Validación personalizada para la contraseña
        RegexValidator(
            regex=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]+$',
            message='La contraseña debe contener al menos una letra mayúscula, una letra minúscula, un número y un carácter especial.'
        )
    ],
    help_text='La contraseña debe contener al menos una letra mayúscula, una letra minúscula, un número y un carácter especial.'
)
    
    mail = forms.CharField(label='Correo Electrónico', validators=[EmailValidator(message='Por favor, introduce un correo electrónico válido.')])
    

    def clean_mail(self):
        mail = self.cleaned_data['mail']
        
        try:
            domain = mail.split('@')[1]
            mx_records = dns.resolver.resolve(domain, 'MX')
        except dns.resolver.NoAnswer:  # Corrige la excepción aquí
            raise ValidationError("La dirección de correo electrónico no tiene registros MX válidos.")
        except Exception as e:
            raise ValidationError("No se pudo validar el correo electrónico.")

        if User.objects.filter(mail=mail).exists():
            raise ValidationError("Este correo electrónico ya está en uso.")

        return mail

    def clean_dni(self):
        dni = self.cleaned_data['dni']
        if len(dni) < 7 or len(dni) > 8:
            raise ValidationError("El DNI debe contener entre 7 y 8 dígitos.")
        if not dni.isdigit():
            raise ValidationError("El DNI solo puede contener números.")
        return dni

    def clean_cuil_cuit(self):
        cuil_cuit = self.cleaned_data['cuil_cuit']
        if len(cuil_cuit) < 11 or len(cuil_cuit) > 13:
            raise ValidationError("El CUIL/CUIT debe contener entre 11 y 13 caracteres.")
        if not cuil_cuit.replace('-', '').isdigit():
            raise ValidationError("El CUIL/CUIT solo puede contener números y guiones.")
        return cuil_cuit

    def clean_fecha_nacimiento(self):
        fecha_nacimiento = self.cleaned_data.get('fecha_nacimiento')
        if fecha_nacimiento:
            today = date.today()
            edad = today.year - fecha_nacimiento.year - ((today.month, today.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
            if edad < 18:
                raise ValidationError("Debes ser mayor de edad para registrarte.")
            return fecha_nacimiento  # Devuelve la fecha de nacimiento validada
        return None

    def save(self, commit=True):
        user = super().save(commit=False)
        user.tipo = 'Usuario'
        if commit:
            user.save()
        return user
    
    field_order = ['nombre', 'apellido', 'dni', 'fecha_nacimiento', 'fecha_expiracion_dni', 'nacionalidad', 'genero', 'domicilio', 'cuil_cuit', 'mail', 'password']

