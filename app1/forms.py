from django import forms
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from .models import Clientes, Encargado, Vehiculo
from django.forms import inlineformset_factory

# Formulario de autenticación personalizado que permite autenticación por email o nombre de usuario.
class CustomAuthenticationForm(forms.Form):
    username_or_email = forms.CharField(label="Usuario o Email")
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)

    # Método para limpiar y validar los datos ingresados.
    def clean(self):
        cleaned_data = super().clean()
        username_or_email = cleaned_data.get("username_or_email")
        password = cleaned_data.get("password")
        
        # Validar que los campos no estén vacíos.
        if not username_or_email:
            raise ValidationError("El campo de usuario o correo electrónico no puede estar vacío.")
        
        user = None

        # Verifica si el valor ingresado es un correo electrónico.
        if "@" in username_or_email:
            try:
                # Busca al cliente por email.
                cliente = Clientes.objects.get(email=username_or_email)
                # Depuración: Mostrar contraseñas (esto debería eliminarse en producción).
                print(f"Cliente - Contraseña ingresada: {password}")
                print(f"Cliente - Contraseña cifrada: {cliente.password}")
                if check_password(password, cliente.password):
                    user = cliente
                else:
                    raise ValidationError("Usuario o contraseña incorrectos.")
            except Clientes.DoesNotExist:
                # Si no es cliente, busca al encargado por correo electrónico.
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
            # Si no es un correo, busca por nombre de usuario.
            try:
                cliente = Clientes.objects.get(nombre=username_or_email)
                print(f"Cliente - Contraseña ingresada: {password}")
                print(f"Cliente - Contraseña cifrada: {cliente.password}")
                if check_password(password, cliente.password):
                    user = cliente
                else:
                    raise ValidationError("Usuario o contraseña incorrectos.")
            except Clientes.DoesNotExist:
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
        
        # Si no se encuentra un usuario válido.
        if not user:
            raise ValidationError("Usuario o contraseña incorrectos.")
        
        self.user = user
        return cleaned_data

    # Método para obtener el usuario autenticado.
    def get_user(self):
        return self.user


# Formulario para gestionar clientes con validación de contraseña.
class ClienteForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirmar Contraseña")

    class Meta:
        model = Clientes
        fields = ['nombre', 'email', 'password', 'telefono', 'direccion']

    # Validación para confirmar que las contraseñas coinciden.
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Las contraseñas no coinciden.")
        
        return cleaned_data

    # Método para guardar el cliente y encriptar su contraseña.
    def save(self, commit=True):
        cliente = super().save(commit=False)
        cliente.set_password(self.cleaned_data['password'])
        if commit:
            cliente.save()
        return cliente


# Formulario para gestionar vehículos.
class VehiculoForm(forms.ModelForm):
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


# InlineFormSet para relacionar clientes con sus vehículos, permite agregar o eliminar vehículos.
VehiculoFormSet = inlineformset_factory(Clientes, Vehiculo, form=VehiculoForm, extra=1, can_delete=True)
