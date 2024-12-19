from django import forms
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from .models import Clientes, Encargado, Vehiculo
from django.forms import inlineformset_factory
import re

class CustomAuthenticationForm(forms.Form):
    """
    Formulario de autenticación personalizado que permite el inicio de sesión
    utilizando un nombre de usuario o correo electrónico.

    Campos:
        - username_or_email (CharField): Nombre de usuario o correo electrónico.
        - password (CharField): Contraseña ingresada por el usuario.

    Métodos:
        - clean(): Valida las credenciales y autentica al usuario.
        - get_user(): Devuelve el usuario autenticado.
    """
    username_or_email = forms.CharField(label="Usuario o Email")
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username_or_email = cleaned_data.get("username_or_email")
        password = cleaned_data.get("password")
        
        if not username_or_email:
            raise ValidationError("El campo de usuario o correo electrónico no puede estar vacío.")

        user = None

        # Verifica si es un correo electrónico
        if "@" in username_or_email:
            try:
                cliente = Clientes.objects.get(email=username_or_email)
                if check_password(password, cliente.password):
                    user = cliente
                else:
                    raise ValidationError("Usuario o contraseña incorrectos.")
            except Clientes.DoesNotExist:
                try:
                    encargado = Encargado.objects.get(correo=username_or_email)
                    if check_password(password, encargado.password):
                        user = encargado
                    else:
                        raise ValidationError("Usuario o contraseña incorrectos.")
                except Encargado.DoesNotExist:
                    raise ValidationError("Usuario o contraseña incorrectos.")
        else:
            try:
                cliente = Clientes.objects.get(nombre=username_or_email)
                if check_password(password, cliente.password):
                    user = cliente
                else:
                    raise ValidationError("Usuario o contraseña incorrectos.")
            except Clientes.DoesNotExist:
                try:
                    encargado = Encargado.objects.get(nombre=username_or_email)
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
        """ Devuelve el usuario autenticado. """
        return self.user

class ClienteForm(forms.ModelForm):
    """
    Formulario de registro para clientes.

    Campos:
        - nombre: Nombre del cliente.
        - email: Correo electrónico.
        - password: Contraseña del cliente.
        - confirm_password: Confirmación de la contraseña.
        - telefono: Teléfono del cliente.
        - direccion: Dirección del cliente.

    Métodos:
        - clean(): Verifica que las contraseñas coincidan y valida la robustez de la contraseña.
        - validate_password_strength(): Verifica que la contraseña cumpla con requisitos mínimos de seguridad.
        - save(): Cifra la contraseña antes de guardar el cliente.
    """
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirmar Contraseña")

    class Meta:
        model = Clientes
        fields = ['nombre', 'email', 'password', 'telefono', 'direccion']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Las contraseñas no coinciden.")
        
        if password:
            self.validate_password_strength(password)

        return cleaned_data

    def validate_password_strength(self, password):
        """ Valida que la contraseña cumpla con requisitos de seguridad. """
        if len(password) < 8:
            raise ValidationError("La contraseña debe tener al menos 8 caracteres.")
        if not re.search(r'[A-Z]', password):
            raise ValidationError("Debe contener al menos una letra mayúscula.")
        if not re.search(r'[a-z]', password):
            raise ValidationError("Debe contener al menos una letra minúscula.")
        if not re.search(r'[0-9]', password):
            raise ValidationError("Debe contener al menos un número.")
        if not re.search(r'[@$!%*?&]', password):
            raise ValidationError("Debe contener al menos un carácter especial (@, $, !, %, *, ?, &).")

    def save(self, commit=True):
        cliente = super().save(commit=False)
        cliente.set_password(self.cleaned_data['password'])
        if commit:
            cliente.save()
        return cliente

class VehiculoForm(forms.ModelForm):
    """
    Formulario para la gestión de vehículos.

    Campos:
        - marca: Marca del vehículo.
        - modelo: Modelo del vehículo.
        - year: Año de fabricación.
        - patente: Matrícula del vehículo.

    Métodos:
        - clean_marca(): Valida que la marca no esté vacía.
        - clean_modelo(): Valida que el modelo no esté vacío.
    """
    class Meta:
        model = Vehiculo
        fields = ['marca', 'modelo', 'year', 'patente']

    def clean_marca(self):
        marca = self.cleaned_data.get('marca')
        if not marca:
            raise forms.ValidationError("Este campo es obligatorio.")
        return marca

    def clean_modelo(self):
        modelo = self.cleaned_data.get('modelo')
        if not modelo:
            raise forms.ValidationError("Este campo es obligatorio.")
        return modelo

VehiculoFormSet = inlineformset_factory(Clientes, Vehiculo, form=VehiculoForm, extra=1, can_delete=True)  
"""
Formulario en línea para gestionar vehículos asociados a un cliente.
Permite agregar, editar o eliminar vehículos.
"""
