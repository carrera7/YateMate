from django import forms
from .models import Publicacion_Amarra as Amarra
from django.core.exceptions import ValidationError
from Amarra.models  import Publicacion_Amarra
from datetime import date, timedelta

class AmarraForm(forms.ModelForm):
    precio = forms.FloatField (label='Precio', widget=forms.TextInput(), required=True)
    cant_dias = forms.CharField (label='Cantidad de dias', widget=forms.TextInput(), required=True)
    ubicacion = forms.CharField(label='Ubicacion', widget=forms.TextInput())   
    
    class Meta:
        model = Publicacion_Amarra
        fields = ['fecha_inicio','cant_dias','precio','ubicacion']

    
    def __init__(self, usuario=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.usuario = usuario
    
    def calcular_fecha_fin(fecha_inicio, duracion_dias):
        fecha_fin = fecha_inicio + timedelta(days=duracion_dias)
        return fecha_fin

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.usuario:
            instance.dueño = self.usuario  # Asigna el usuario activo como el dueño
        if commit:
            instance.save()
        return instance
    def clean(self):
        cleaned_data = super().clean()
        cant_dias = cleaned_data.get('cant_dias')
        fecha_inicio = cleaned_data.get('fecha_inicio')
        ubicacion = cleaned_data.get('ubicacion')

        if Amarra.objects.filter(fecha_inicio=fecha_inicio, ubicacion=ubicacion).exists():
            raise ValidationError("Ya existe una publicación con la misma fecha de inicio y ubicación.")

        # Setear cantidad de días disponibles con el valor de cant_dias
        self.instance.cant_dias_disponibles = cant_dias

        return cleaned_data
    

    