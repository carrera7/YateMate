from django import forms
from .models import Publicacion_Amarra as Amarra
from django.core.exceptions import ValidationError
from Amarra.models  import Publicacion_Amarra
from datetime import date, timedelta

class AmarraForm(forms.ModelForm):
    precio = forms.FloatField (label='Etiqueta', widget=forms.TextInput(), required=True)
    fecha_incio = forms.DateField (label='Etiqueta', widget=forms.TextInput(), required=True)
    cant_dias = forms.FloatField (label='Etiqueta', widget=forms.TextInput(), required=True)
    ubicacion = forms.CharField(label='Etiqueta', widget=forms.TextInput())
    

    class Meta:
        model = Amarra
        fields = ['dueño','fecha_inicio','cant_dias','precio','ubicacion']

    def clean_dueno(self):
        dueño = self.cleaned_data['dueño']
        if dueño.tipo != 'Cliente':
            raise forms.ValidationError("El dueño debe ser un usuario de tipo Cliente.")
        return dueño
    
    def __init__(self, usuario, *args, **kwargs):
        super(Publicacion_Amarra, self).__init__(*args, **kwargs)
        self.fields['dueño'].queryset = Amarra.objects.filter(dueno=usuario) \
            .exclude(publicacion_embarcacion__isnull=False)
    
    def calcular_fecha_fin(fecha_inicio, duracion_dias):
        fecha_fin = fecha_inicio + timedelta(days=duracion_dias)
        return fecha_fin

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance
    

    