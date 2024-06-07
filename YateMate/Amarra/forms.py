from django import forms
from .models import Publicacion_Amarra as Amarra
from django.core.exceptions import ValidationError
from Amarra.models  import Publicacion_Amarra
from datetime import date, timedelta

class AmarraForm(forms.ModelForm):
    precio = forms.FloatField (label='Precio', widget=forms.TextInput(), required=True)
    cant_dias = forms.FloatField (label='Cantidad de dias', widget=forms.TextInput(), required=True)
    ubicacion = forms.CharField(label='Ubicacion', widget=forms.TextInput())
    cant_dias_disponibles= forms.IntegerField(label="Cantidad dias disponibles", widget=forms.TextInput())    
    
    class Meta:
        model = Publicacion_Amarra
        fields = ['dueño','fecha_inicio','cant_dias','precio','ubicacion','cant_dias_disponibles']

    def clean_dueno(self):
        dueño = self.cleaned_data['dueño']
        if dueño.tipo != 'Cliente':
            raise forms.ValidationError("El dueño debe ser un usuario de tipo Cliente.")
        return dueño
    
    def __init__(self, usuario, *args, **kwargs):
        super().__init__(*args, **kwargs)
       # self.fields['dueño'].queryset = Amarra.objects.filter(dueño=usuario) 
    
    def calcular_fecha_fin(fecha_inicio, duracion_dias):
        fecha_fin = fecha_inicio + timedelta(days=duracion_dias)
        return fecha_fin

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance
    

    