from django import forms
from django.core.exceptions import ValidationError
from Register.models import User

class CustomUserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'edad', 'password']

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nombre de usuario ya está en uso.")
        return username

    def clean_edad(self):
        edad = self.cleaned_data['edad']
        if edad < 18:
            raise forms.ValidationError("Debes ser mayor de edad para registrarte.")
        return edad      

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user
