from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

class CustomAuthenticationForm(forms.Form):
    username_or_email = forms.CharField(label="Usuario o Email")
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username_or_email = cleaned_data.get("username_or_email")
        password = cleaned_data.get("password")
        
        # Asegurarse de que username_or_email no sea None ni vacío
        if not username_or_email:
            raise ValidationError("El campo de usuario o correo electrónico no puede estar vacío.")
        
        user = None

        # Verificar si es un email
        if "@" in username_or_email:
            try:
                # Buscar el usuario por email
                user_obj = User.objects.get(email=username_or_email)
                # Intentar autenticar usando el nombre de usuario encontrado
                user = authenticate(username=user_obj.username, password=password)
            except User.DoesNotExist:
                raise ValidationError("Usuario o contraseña incorrectos.")
        else:
            # Intentar autenticar usando solo el nombre de usuario
            user = authenticate(username=username_or_email, password=password)
        
        if not user:
            raise ValidationError("Usuario o contraseña incorrectos.")
        
        self.user = user
        return cleaned_data

    def get_user(self):
        return self.user