# blog/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    nombre = forms.CharField(max_length=100)
    edad = forms.IntegerField()
    curso = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['username', 'nombre', 'edad', 'curso', 'password1', 'password2']

# Nuevo formulario para almacenar APT1 y APT2
class RespuestaForm(forms.Form):
    APT1 = forms.CharField(max_length=255, required=False)
    APT2 = forms.CharField(max_length=255, required=False)
