from datetime import date
import re
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator, MinLengthValidator, RegexValidator
import dns
import dns.resolver
from Register.models import User
from django import forms
from django.forms import DateInput

class CustomDateInput(DateInput):
    input_type = 'date'

    def __init__(self, **kwargs):
        kwargs['format'] = '%d-%m-%Y'
        super().__init__(**kwargs)

class CustomUserRegistrationForm(forms.ModelForm):
    mail = forms.CharField(label='Correo Electrónico',
                           validators=[EmailValidator(message='Por favor, introduce un correo electrónico válido.')],
                           error_messages={'required': 'Este campo es obligatorio',
                                           'invalid': 'Por favor, introduce un correo electrónico válido'})

    class Meta:
        model = User
        fields = ['mail', 'password', 'nombre', 'apellido', 'dni', 'fecha_nacimiento', 'fecha_expiracion_dni',
                  'nacionalidad', 'genero', 'domicilio', 'cuil_cuit']
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
        widgets = {
            'fecha_nacimiento': CustomDateInput(),  # Usando el CustomDateInput para el campo de fecha_nacimiento
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
        help_text='La contraseña debe contener al menos una letra mayúscula, una letra minúscula, un número y un carácter especial.',
        error_messages={
            'min_length': 'La contraseña debe tener al menos 8 caracteres.',
            'required': 'Este campo es obligatorio.'
        }
    )

    fecha_nacimiento = forms.DateField(
        label='Fecha de Nacimiento',
        error_messages={
            'required': 'Este campo es obligatorio',
            'invalid': 'Introduce una fecha válida en el formato DD-MM-AAAA'
        },
        help_text='Formato: DD-MM-AAAA. Ejemplo: 01/02/1990'
    )

    fecha_expiracion_dni = forms.DateField(
        label='Fecha de Expiracion DNI',
        error_messages={
            'required': 'Este campo es obligatorio',
            'invalid': 'Introduce una fecha válida en el formato DD-MM-AAAA'
        },
        help_text='Formato: DD-MM-AAAA. Ejemplo: 01/02/1990'
    )

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
            edad = today.year - fecha_nacimiento.year - (
                    (today.month, today.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
            if edad < 18:
                raise ValidationError("Debes ser mayor de edad para registrarte.")
            return fecha_nacimiento
