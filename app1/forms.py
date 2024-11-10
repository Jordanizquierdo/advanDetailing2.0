# forms.py
from django import forms
from .models import Encargado, Cliente, Vehiculo, Servicio, Reserva, Review
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Password", 
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label="Confirm Password", 
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords do not match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user




class EncargadoForm(forms.ModelForm):
    class Meta:
        model = Encargado
        fields = ['usuario', 'nombre', 'telefono', 'correo']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre'}),
            'telefono': forms.TextInput(attrs={'placeholder': 'Teléfono'}),
            'correo': forms.EmailInput(attrs={'placeholder': 'Correo electrónico'}),
        }

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['usuario', 'nombre', 'telefono', 'direccion']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre'}),
            'telefono': forms.TextInput(attrs={'placeholder': 'Teléfono'}),
            'direccion': forms.TextInput(attrs={'placeholder': 'Dirección'}),
        }

class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = ['marca', 'modelo', 'year', 'patente']
        widgets = {
            'marca': forms.TextInput(attrs={'placeholder': 'Marca'}),
            'modelo': forms.TextInput(attrs={'placeholder': 'Modelo'}),
            'year': forms.TextInput(attrs={'placeholder': 'Año'}),
            'patente': forms.TextInput(attrs={'placeholder': 'Patente'}),
        }

class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = ['nombre', 'descripcion', 'precio', 'duracion']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre del servicio'}),
            'descripcion': forms.Textarea(attrs={'placeholder': 'Descripción', 'rows': 3}),
            'precio': forms.NumberInput(attrs={'placeholder': 'Precio'}),
            'duracion': forms.TextInput(attrs={'placeholder': 'Duración'}),
        }

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['hora_reserva', 'fecha_reserva', 'estado', 'administrador', 'servicio', 'cliente', 'vehiculo']
        widgets = {
            'hora_reserva': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'fecha_reserva': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'estado': forms.TextInput(attrs={'placeholder': 'Estado'}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comentarios', 'calificacion', 'fecha_review', 'cliente', 'vehiculo']
        widgets = {
            'comentarios': forms.Textarea(attrs={'placeholder': 'Comentarios', 'rows': 3}),
            'calificacion': forms.NumberInput(attrs={'placeholder': 'Calificación', 'min': 1, 'max': 5}),
            'fecha_review': forms.DateInput(attrs={'type': 'date'}),
        }
