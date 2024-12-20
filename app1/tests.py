from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.hashers import check_password
from .models import Clientes, Vehiculo, Reservas, Servicios
import json


class SystemTestRegisterLoginReservationAddVehicle(TestCase):
    """
    Pruebas integrales para registrar un cliente, iniciar sesión, agregar un vehículo
    y realizar una reserva en el sistema.

    Métodos de prueba:
        setUp(): Configuración inicial para crear objetos necesarios.
        test_full_user_flow(): Prueba completa que verifica el flujo del usuario desde el registro
        hasta la creación de una reserva.
    """
    def setUp(self):
        """
        Configuración inicial para las pruebas. Crea un cliente HTTP y un servicio de ejemplo.
        """
        self.client = Client()

        # Crear un servicio de ejemplo
        self.servicio = Servicios.objects.create(
            nombre_servicio="Grabado de patente",
            descripcion="Grabado de patente en los vidrios",
            precio=20000
        )

    def test_full_user_flow(self):
        """
        Prueba integral que cubre el registro, inicio de sesión, agregar un vehículo
        y realizar una reserva.

        Verifica:
        - Registro exitoso y redirección al login.
        - Inicio de sesión exitoso y creación de sesión.
        - Adición de un vehículo y redirección a la vista correspondiente.
        - Creación de una reserva asociada al vehículo y servicio especificado.
        """
        # 1. Registrar un cliente
        register_data = {
            'nombre': 'Nuevo Cliente',
            'email': 'nuevo.cliente@test.com',
            'telefono': '123456789',
            'direccion': 'Calle Falsa 123',
            'password': 'cliente123',
            'confirm_password': 'cliente123'
        }
        response = self.client.post(reverse('register'), register_data)

        # Verificar que se redirige al login después del registro
        self.assertEqual(response.status_code, 302, f"Registro fallido: {response.content.decode()}")
        self.assertRedirects(response, reverse('login'))

        # Verificar que el cliente fue creado en la base de datos
        cliente = Clientes.objects.get(email='nuevo.cliente@test.com')
        self.assertEqual(cliente.nombre, 'Nuevo Cliente')
        self.assertTrue(cliente.check_password('cliente123'))

        # 2. Iniciar sesión con el nuevo cliente
        login_data = {
            'email': 'nuevo.cliente@test.com',
            'password': 'cliente123'
        }
        response = self.client.post(reverse('login'), login_data)

        # Verificar que se redirige al home después del login
        self.assertEqual(response.status_code, 302, f"Inicio de sesión fallido: {response.content.decode()}")
        self.assertRedirects(response, reverse('home'))

        # Verificar que la sesión del cliente se inició correctamente
        session = self.client.session
        self.assertIn('cliente_id', session)
        self.assertEqual(session['cliente_id'], cliente.id)

        # 3. Agregar un vehículo
        vehicle_data = {
            'marca': 'Toyota',
            'modelo': 'Corolla',
            'year': 2022,
            'patente': 'XYZ78'
        }
        response = self.client.post(reverse('agregar_vehiculo'), vehicle_data)

        # Verificar que se redirige a la página de vehículos después de agregar uno
        self.assertEqual(response.status_code, 302, f"Agregar vehículo fallido: {response.content.decode()}")
        self.assertRedirects(response, reverse('mis_vehiculos'))

        # Verificar que el vehículo fue agregado a la base de datos
        vehiculo = Vehiculo.objects.get(patente='XYZ78')
        self.assertEqual(vehiculo.marca, 'Toyota')
        self.assertEqual(vehiculo.modelo, 'Corolla')
        self.assertEqual(vehiculo.cliente, cliente)

        # 4. Realizar una reserva con el vehículo y un servicio
        reserva_data = {
            'fecha_reserva': '2024-12-20',
            'hora_reserva': '19:00',
            'vehiculo': vehiculo.id,
            'cartList': json.dumps([{'id': self.servicio.id, 'price': self.servicio.precio}])
        }
        response = self.client.post(reverse('carrito'), reserva_data)

        # Verificar que se redirige al home después de realizar una reserva
        self.assertEqual(response.status_code, 302, f"Reserva fallida: {response.content.decode()}")
        self.assertRedirects(response, reverse('home'))

        # Verificar que la reserva fue creada correctamente
        reserva = Reservas.objects.filter(cliente=cliente).first()
        self.assertIsNotNone(reserva, "No se creó la reserva en la base de datos.")
        self.assertEqual(reserva.vehiculo, vehiculo)
        self.assertIn(self.servicio, reserva.servicios.all())
