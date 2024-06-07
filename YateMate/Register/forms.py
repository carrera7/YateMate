from django import forms
from .models import Embarcacion, User
from django.core.exceptions import ValidationError
import re

class EmbarcacionForm(forms.ModelForm):
    tipo = forms.ChoiceField(choices=Embarcacion.TIPOS, required=True)
    foto = forms.ImageField(label='Foto', required=True)
    eslora = forms.FloatField(label='Eslora (metros)', min_value=0.1, required=True)
    manga = forms.FloatField(label='Manga (metros)', min_value=0.1, required=True)
    calado = forms.FloatField(label='Calado (metros)', min_value=0.1, required=True)
    matricula = forms.CharField(label='Matrícula', max_length=20, required=True)

    class Meta:
        model = Embarcacion
        fields = ['tipo', 'eslora', 'manga', 'calado', 'matricula', 'nombre_fantasia', 'foto', 'dueno']

    def clean_matricula(self):
        matricula = self.cleaned_data['matricula']
        if not re.match(r'^[A-Za-z0-9]+$', matricula):
            raise forms.ValidationError("La matrícula solo puede contener letras y números.")
        if Embarcacion.objects.filter(matricula=matricula).exists():
            raise forms.ValidationError("¡La matrícula ingresada ya está en uso! Por favor, elija otra.")

        return matricula

    def clean_dueno(self):
        dueno = self.cleaned_data['dueno']
        if dueno.tipo != 'Cliente':
            raise forms.ValidationError("El dueño debe ser un usuario de tipo Cliente.")
        return dueno

    def clean_foto(self):
        foto = self.cleaned_data.get('foto', False)
        if foto:
            if foto.size > 1024 * 1024:  # 1MB
                raise forms.ValidationError("La imagen es demasiado grande (máximo 1MB).")
            return foto
        else:
            raise forms.ValidationError("Debe subir una imagen válida.")

    def __init__(self, *args, **kwargs):
        super(EmbarcacionForm, self).__init__(*args, **kwargs)
        # Filtrar los usuarios de tipo Cliente en el campo de dueño
        self.fields['dueno'].queryset = User.objects.filter(tipo='Cliente')
