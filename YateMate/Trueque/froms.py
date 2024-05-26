# forms.py en myapp
from django import forms
from .models import Publicacion_ObjetoValioso,Publicacion_Embarcacion
from Register.models import Embarcacion


class PublicacionObjetoValiosoForm(forms.ModelForm):
    class Meta:
        model = Publicacion_ObjetoValioso
        fields = ['tipo', 'marca', 'descripcion', 'foto']  # No incluimos 'dueño' ni 'estado' en los fields

    def __init__(self, usuario, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.usuario = usuario  # Guardamos el usuario para usarlo en el método save

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.dueño = self.usuario  # Asignamos el dueño basado en el usuario pasado al formulario
        instance.estado = 'Vigente'  # Asignamos el estado 'Vigente'
        if commit:
            instance.save()
        return instance

class PublicacionEmbarcacionForm(forms.ModelForm):
    class Meta:
        model = Publicacion_Embarcacion
        fields = ['embarcacion', 'descripcion']

    def __init__(self, usuario, *args, **kwargs):
        super(PublicacionEmbarcacionForm, self).__init__(*args, **kwargs)
        self.fields['embarcacion'].queryset = Embarcacion.objects.filter(dueno=usuario) \
            .exclude(publicacion_embarcacion__isnull=False)
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.estado = 'Vigente'  # Asignamos el estado 'Vigente'
        if commit:
            instance.save()
        return instance