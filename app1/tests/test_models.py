from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.hashers import check_password
from app1.models import Encargado, Clientes, Vehiculo, Servicios, Reservas, Reviews

class EncargadoModelTest(TestCase):
    def test_create_encargado(self):
        encargado = Encargado.objects.create(
            nombre="Juan",
            apellido="Perez",
            correo="juan@example.com",
            telefono="123456789"
        )
        encargado.set_password("password123")
        self.assertTrue(check_password("password123", encargado.password))
        self.assertEqual(str(encargado), "Juan Perez")

class ClientesModelTest(TestCase):
    def test_create_cliente(self):
        cliente = Clientes.objects.create(
            nombre="Maria",
            email="maria@example.com",
            telefono="987654321",
            direccion="Calle 123",
            fecha_registro=timezone.now()
        )
        cliente.set_password("mypassword")
        self.assertTrue(check_password("mypassword", cliente.password))
        self.assertEqual(str(cliente), "Maria")

class VehiculoModelTest(TestCase):
    def test_create_vehiculo(self):
        cliente = Clientes.objects.create(
            nombre="Carlos",
            email="carlos@example.com",
            telefono="555444333",
            direccion="Avenida 456"
        )
        vehiculo = Vehiculo.objects.create(
            cliente=cliente,
            marca="Toyota",
            modelo="Corolla",
            year="2020",
            patente="ABC12"
        )
        self.assertEqual(str(vehiculo), "Toyota Corolla (ABC12)")
        self.assertEqual(vehiculo.cliente.nombre, "Carlos")

class ServiciosModelTest(TestCase):
    def test_create_servicio(self):
        servicio = Servicios.objects.create(
            nombre_servicio="Lavado Básico",
            descripcion="Lavado exterior del vehículo",
            precio=15000,
            duracion="30 minutos"
        )
        self.assertEqual(str(servicio), "Lavado Básico")

class ReservasModelTest(TestCase):
    def test_create_reserva(self):
        encargado = Encargado.objects.create(
            nombre="Sofia",
            apellido="Gomez",
            correo="sofia@example.com",
            telefono="123123123"
        )
        cliente = Clientes.objects.create(
            nombre="Ana",
            email="ana@example.com",
            telefono="456456456",
            direccion="Calle Falsa 123"
        )
        vehiculo = Vehiculo.objects.create(
            cliente=cliente,
            marca="Honda",
            modelo="Civic",
            year="2019",
            patente="XYZ99"
        )
        servicio1 = Servicios.objects.create(
            nombre_servicio="Lavado Premium",
            descripcion="Lavado completo interior y exterior",
            precio=30000,
            duracion="1 hora"
        )
        servicio2 = Servicios.objects.create(
            nombre_servicio="Encerado",
            descripcion="Protección con cera para pintura",
            precio=20000,
            duracion="45 minutos"
        )
        reserva = Reservas.objects.create(
            hora_reserva=timezone.now(),
            fecha_reserva=timezone.now(),
            estado="confirmada",
            administrador=encargado,
            cliente=cliente,
            vehiculo=vehiculo
        )
        reserva.servicios.set([servicio1, servicio2])
        self.assertEqual(reserva.administrador.nombre, "Sofia")
        self.assertEqual(reserva.cliente.nombre, "Ana")
        self.assertEqual(reserva.vehiculo.marca, "Honda")
        self.assertIn(servicio1, reserva.servicios.all())
        self.assertEqual(
            str(reserva), "Reserva de Ana para Lavado Premium, Encerado"
        )

class ReviewsModelTest(TestCase):
    def test_create_review(self):
        cliente = Clientes.objects.create(
            nombre="Lucas",
            email="lucas@example.com",
            telefono="999888777",
            direccion="Plaza Mayor 789"
        )
        vehiculo = Vehiculo.objects.create(
            cliente=cliente,
            marca="Mazda",
            modelo="3",
            year="2021",
            patente="LMN45"
        )
        review = Reviews.objects.create(
            comentarios="Excelente servicio y atención.",
            calificacion=5,
            fecha_review=timezone.now(),
            cliente=cliente,
            vehiculo=vehiculo
        )
        self.assertEqual(review.cliente.nombre, "Lucas")
        self.assertEqual(review.vehiculo.marca, "Mazda")
        self.assertEqual(str(review), "Review de Lucas para Mazda 3 (LMN45)")
