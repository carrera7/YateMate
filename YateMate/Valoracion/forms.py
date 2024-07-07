# forms.py
from django import forms
from .models import Valoracion_Trueque, Valoracion_Amarra

class ValoracionTruequeForm(forms.ModelForm):
    estrellas = forms.IntegerField(min_value=0, max_value=5, label='Estrellas'  )
    comentario = forms.CharField(widget=forms.Textarea, label='Comentario')

    class Meta:
        model = Valoracion_Trueque
        fields = ['estrellas', 'comentario']

class ValoracionAmarraForm(forms.ModelForm):
    estrellas = forms.IntegerField(min_value=0, max_value=5, label='Estrellas')
    comentario = forms.CharField(widget=forms.Textarea, label='Comentario')

    class Meta:
        model = Valoracion_Amarra
        fields = ['estrellas', 'comentario']
        

class RespuestaValoracionForm(forms.ModelForm):
    class Meta:
        model = Valoracion_Trueque
        fields = ['respuesta']
        labels = {'respuesta': 'Agregar Respuesta'}

class RespuestaValoracionAmarraForm(forms.ModelForm):
    class Meta:
        model = Valoracion_Amarra
        fields = ['respuesta']
        labels = {'respuesta': 'Agregar Respuesta'}
