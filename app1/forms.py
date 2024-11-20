from django import forms
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from .models import Clientes, Encargado,Vehiculo
from django.forms import inlineformset_factory
# esto esta cambiado
class CustomAuthenticationForm(forms.Form):
    email = forms.CharField(label="Email")
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if not email:
            self.add_error('email', "Por favor, ingresa tu correo.")
        if not password:
            self.add_error('password', "Por favor, ingresa tu contraseña.")

        user = None

        try:
            cliente = Clientes.objects.get(email__iexact=email)
            if check_password(password, cliente.password):
                user = cliente
        except Clientes.DoesNotExist:
            try:
                encargado = Encargado.objects.get(correo__iexact=email)
                if check_password(password, encargado.password):
                    user = encargado
            except Encargado.DoesNotExist:
                pass

        if not user:
            raise ValidationError("Correo o contraseña incorrectos.")

        self.user = user
        return cleaned_data

    def get_user(self):
        return self.user



# esto tambien cambiado
class ClienteForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'required': 'true'}), label="Contraseña")
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'required': 'true'}), label="Confirmar Contraseña")

    class Meta:
        model = Clientes
        fields = ['nombre', 'email', 'password', 'telefono', 'direccion']
        widgets = {
            'nombre': forms.TextInput(attrs={'required': 'true'}),
            'email': forms.EmailInput(attrs={'required': 'true'}),
            'telefono': forms.TextInput(attrs={'required': 'true'}),
            'direccion': forms.TextInput(attrs={'required': 'true'}),
        }

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

#igual que este.
class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = ['marca', 'modelo', 'year', 'patente']
        widgets = {
            'marca': forms.TextInput(attrs={'required': 'true'}),
            'modelo': forms.TextInput(attrs={'required': 'true'}),
            'year': forms.TextInput(attrs={'required': 'true'}),
            'patente': forms.TextInput(attrs={'required': 'true'}),
        }

VehiculoFormSet = inlineformset_factory(
    Clientes,
    Vehiculo,
    form=VehiculoForm,
    extra=1,
    can_delete=True
)
