from django import forms
from  Register.models import User

class CustomUserRegistrationForm(forms.Form):
    username = forms.EmailField()
    age = forms.IntegerField()
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nombre de usuario ya está en uso.")
        return username

    def clean_age(self):
        age = self.cleaned_data['age']
        if age < 18:
            raise forms.ValidationError("Debes ser mayor de edad para registrarte.")
        return age      

    def save(self, commit=True):
            user = User.objects.create_user(
                username=self.cleaned_data['username'],
                password=self.cleaned_data['password'],
            )
            user.age = self.cleaned_data['age']
            if commit:
                user.save()
            return user
