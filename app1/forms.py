from django import forms
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from .models import Clientes, Encargado,Vehiculo
from django.forms import inlineformset_factory

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



class ClienteForm(forms.ModelForm):
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
        
        return cleaned_data

    def save(self, commit=True):
        cliente = super().save(commit=False)
        cliente.set_password(self.cleaned_data['password'])
        if commit:
            cliente.save()
        return cliente

class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = ['marca', 'modelo', 'year', 'patente']

VehiculoFormSet = inlineformset_factory(Clientes, Vehiculo, form=VehiculoForm, extra=1, can_delete=True)
