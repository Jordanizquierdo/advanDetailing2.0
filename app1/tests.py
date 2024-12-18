from django.test import TestCase
from django.contrib.auth.hashers import make_password
from .forms import CustomAuthenticationForm, ClienteForm, VehiculoForm
from .models import Clientes, Encargado
from django.core.exceptions import ValidationError
from django import forms


class CustomAuthenticationFormTest(TestCase):
    def setUp(self):
        # Crear datos de prueba
        self.cliente = Clientes.objects.create(
            nombre="Juan",
            email="juan@example.com",
            password=make_password("password123"),
            telefono="123456789",
            direccion="Calle Falsa 123",
        )
        self.encargado = Encargado.objects.create(
            nombre="Admin",
            apellido="Apellido",
            password=make_password("adminpassword"),
            correo="admin@example.com",
            telefono="987654321",
        )

    def test_valid_login_with_email(self):
        """Prueba un login válido usando el email del cliente"""
        form_data = {"username_or_email": "juan@example.com", "password": "password123"}
        form = CustomAuthenticationForm(data=form_data)
        self.assertTrue(form.is_valid(), "El formulario no es válido con un email y contraseña correctos.")
        self.assertEqual(form.get_user(), self.cliente, "El usuario autenticado no coincide con el cliente esperado.")

    def test_valid_login_with_username(self):
        """Prueba un login válido usando el nombre del cliente"""
        form_data = {"username_or_email": "Juan", "password": "password123"}
        form = CustomAuthenticationForm(data=form_data)
        self.assertTrue(form.is_valid(), "El formulario no es válido con un nombre de usuario y contraseña correctos.")
        self.assertEqual(form.get_user(), self.cliente, "El usuario autenticado no coincide con el cliente esperado.")

    def test_invalid_login(self):
        """Prueba un login inválido con una contraseña incorrecta"""
        form_data = {"username_or_email": "juan@example.com", "password": "wrongpassword"}
        form = CustomAuthenticationForm(data=form_data)
        self.assertFalse(form.is_valid(), "El formulario es válido con credenciales incorrectas.")
        self.assertIn("Usuario o contraseña incorrectos.", form.errors["__all__"], "No se encontró el error esperado en el formulario.")


class ClienteFormTest(TestCase):
    def test_valid_cliente_form(self):
        """Prueba si el formulario ClienteForm es válido con datos correctos"""
        form_data = {
            'nombre': 'Cliente Prueba',
            'email': 'cliente@test.com',
            'password': 'Password123@',
            'confirm_password': 'Password123@',
            'telefono': '123456789',
            'direccion': 'Calle Falsa 123',
        }
        form = ClienteForm(data=form_data)
        self.assertTrue(form.is_valid(), "El formulario no es válido con datos correctos.")

    def test_passwords_do_not_match(self):
        """Prueba si el formulario rechaza contraseñas que no coinciden"""
        form_data = {
            "nombre": "Juan",
            "email": "juan@example.com",
            "password": "password123",
            "confirm_password": "password456",
            "telefono": "123456789",
            "direccion": "Calle Falsa 123",
        }
        form = ClienteForm(data=form_data)
        self.assertFalse(form.is_valid(), "El formulario es válido con contraseñas que no coinciden.")
        self.assertIn("Las contraseñas no coinciden.", form.errors["confirm_password"], "No se encontró el error esperado para contraseñas que no coinciden.")

    def test_invalid_cliente_form_weak_password(self):
        """Prueba que el formulario ClienteForm rechace contraseñas débiles"""
        form_data = {
            'nombre': 'Cliente Prueba',
            'email': 'cliente@test.com',
            'password': '123456',
            'confirm_password': '123456',
            'telefono': '123456789',
            'direccion': 'Calle Falsa 123',
        }
        form = ClienteForm(data=form_data)
        self.assertFalse(form.is_valid(), "El formulario es válido con una contraseña débil.")

        # Debugging: Imprimir errores si no están donde se esperan
        if 'password' not in form.errors:
            print("Errores del formulario:", form.errors)

        # Verificar que los errores están en el campo 'password'
        self.assertIn('password', form.errors, "No se encontró el error de validación para contraseña.")
        self.assertIn("La contraseña debe tener al menos 8 caracteres.", form.errors['password'], "El mensaje de error para contraseñas débiles no es el esperado.")


class VehiculoFormTest(TestCase):
    def test_valid_vehiculo_form(self):
        """Prueba si el formulario VehiculoForm es válido con datos correctos"""
        form_data = {
            "marca": "Toyota",
            "modelo": "Corolla",
            "year": "2022",
            "patente": "ABC12",
        }
        form = VehiculoForm(data=form_data)
        self.assertTrue(form.is_valid(), "El formulario VehiculoForm no es válido con datos correctos.")

    def test_marca_required(self):
        """Prueba que el campo marca sea obligatorio"""
        form_data = {
            "marca": "",
            "modelo": "Corolla",
            "year": "2022",
            "patente": "ABC12",
        }
        form = VehiculoForm(data=form_data)
        self.assertFalse(form.is_valid(), "El formulario es válido sin una marca.")
        self.assertIn("Este campo es obligatorio.", form.errors["marca"], "No se encontró el error esperado para el campo 'marca'.")

    def test_modelo_required(self):
        """Prueba que el campo modelo sea obligatorio"""
        form_data = {
            "marca": "Toyota",
            "modelo": "",
            "year": "2022",
            "patente": "ABC12",
        }
        form = VehiculoForm(data=form_data)
        self.assertFalse(form.is_valid(), "El formulario es válido sin un modelo.")
        self.assertIn("Este campo es obligatorio.", form.errors["modelo"], "No se encontró el error esperado para el campo 'modelo'.")
