from django import forms
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from .models import Clientes, Encargado

class CustomAuthenticationForm(forms.Form):
    username_or_email = forms.CharField(label="Usuario o Email")
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username_or_email = cleaned_data.get("username_or_email")
        password = cleaned_data.get("password")
        
        if not username_or_email:
            raise ValidationError("El campo de usuario o correo electrónico no puede estar vacío.")
        
        user = None

        # Verificar si es un email
        if "@" in username_or_email:
            try:
                # Buscar el cliente por email
                cliente = Clientes.objects.get(email=username_or_email)
                # Depuración: Imprimir la contraseña cifrada y la contraseña ingresada
                print(f"Cliente - Contraseña ingresada: {password}")
                print(f"Cliente - Contraseña cifrada: {cliente.password}")
                if check_password(password, cliente.password):
                    user = cliente
                else:
                    raise ValidationError("Usuario o contraseña incorrectos.")
            except Clientes.DoesNotExist:
                # Buscar al encargado si no es cliente
                try:
                    encargado = Encargado.objects.get(correo=username_or_email)
                    print(f"Encargado - Contraseña ingresada: {password}")
                    print(f"Encargado - Contraseña cifrada: {encargado.password}")
                    if check_password(password, encargado.password):
                        user = encargado
                    else:
                        raise ValidationError("Usuario o contraseña incorrectos.")
                except Encargado.DoesNotExist:
                    raise ValidationError("Usuario o contraseña incorrectos.")
        else:
            # Buscar al cliente por nombre de usuario
            try:
                cliente = Clientes.objects.get(nombre=username_or_email)
                print(f"Cliente - Contraseña ingresada: {password}")
                print(f"Cliente - Contraseña cifrada: {cliente.password}")
                if check_password(password, cliente.password):
                    user = cliente
                else:
                    raise ValidationError("Usuario o contraseña incorrectos.")
            except Clientes.DoesNotExist:
                # Buscar al encargado por nombre de usuario
                try:
                    encargado = Encargado.objects.get(nombre=username_or_email)
                    print(f"Encargado - Contraseña ingresada: {password}")
                    print(f"Encargado - Contraseña cifrada: {encargado.password}")
                    if check_password(password, encargado.password):
                        user = encargado
                    else:
                        raise ValidationError("Usuario o contraseña incorrectos.")
                except Encargado.DoesNotExist:
                    raise ValidationError("Usuario o contraseña incorrectos.")
        
        if not user:
            raise ValidationError("Usuario o contraseña incorrectos.")
        
        self.user = user
        return cleaned_data

    def get_user(self):
        return self.user
