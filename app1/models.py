from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """Modelo de usuario extendido para incluir tanto a Clientes como a Encargados."""
    is_cliente = models.BooleanField(default=False)
    is_encargado = models.BooleanField(default=False)

class Clientes(models.Model):
    """Modelo Clientes que se vincula al modelo de usuario Django."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cliente_profile")
    telefono = models.CharField(max_length=45)
    direccion = models.CharField(max_length=45)
    fecha_registro = models.DateTimeField(default=timezone.now)
    vehiculo = models.ForeignKey('Vehiculo', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user.username

class Encargado(models.Model):
    """Modelo Encargado que se vincula al modelo de usuario Django."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="encargado_profile")
    telefono = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"





class Reservas(models.Model):
    hora_reserva = models.DateTimeField()
    fecha_reserva = models.DateTimeField()  # Cambié a DateTimeField para incluir la hora
    estado = models.CharField(max_length=20)
    administrador = models.ForeignKey('Encargado', on_delete=models.SET_NULL, null=True)
    servicio = models.ForeignKey('Servicios', on_delete=models.CASCADE, null=True)
    cliente = models.ForeignKey('Clientes', on_delete=models.CASCADE, null=True)
    vehiculo = models.ForeignKey('Vehiculo', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Reserva de {self.cliente} para {self.servicio}"




class Servicios(models.Model):
    nombre_servicio = models.CharField(max_length=45)
    descripcion = models.CharField(max_length=100)
    precio = models.IntegerField()
    duracion = models.CharField(max_length=45)

    def __str__(self):
        return self.nombre_servicio


class Reviews(models.Model):
    comentarios = models.CharField(max_length=45)
    calificacion = models.IntegerField()  # Cambié a IntegerField para almacenar una calificación numérica
    fecha_review = models.DateField()
    cliente = models.ForeignKey('Clientes', on_delete=models.CASCADE, null=True)
    vehiculo = models.ForeignKey('Vehiculo', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Review de {self.cliente} para {self.vehiculo}"


class Vehiculo(models.Model):
    marca = models.CharField(max_length=45)
    modelo = models.CharField(max_length=45)
    year = models.CharField(max_length=45)
    patente = models.CharField(max_length=5)

    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.patente})"
