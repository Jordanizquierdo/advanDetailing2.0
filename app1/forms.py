from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

    


from django import forms
from django.contrib.auth.forms import AuthenticationForm

class CustomAuthenticationForm(AuthenticationForm):
    """Formulario de autenticación personalizado que hereda de AuthenticationForm de Django."""
    username = forms.CharField(label="Correo o nombre de usuario")
    password = forms.CharField(widget=forms.PasswordInput)
