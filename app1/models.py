from django.db import models
from django.utils import timezone

class Clientes(models.Model):
    nombre = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    telefono = models.CharField(max_length=45)
    direccion = models.CharField(max_length=45)
    fecha_registro = models.DateTimeField(default=timezone.now)
    vehiculo = models.ForeignKey('Vehiculo', on_delete=models.CASCADE, null=True)  # Permitir valores nulos

    def __str__(self):
        return self.nombre


class Reservas(models.Model):
    hora_reserva = models.DateTimeField()
    fecha_reserva = models.DateField()
    estado = models.CharField(max_length=20)
    administrador = models.ForeignKey('Encargado', on_delete=models.SET_NULL, null=True)
    servicio = models.ForeignKey('Servicios', on_delete=models.CASCADE, null=True)
    cliente = models.ForeignKey('Clientes', on_delete=models.CASCADE, null=True)  # Permitir valores nulos temporalmente
    vehiculo = models.ForeignKey('Vehiculo', on_delete=models.CASCADE, null=True)  # Si ya es anulable

    def __str__(self):
        return f"Reserva de {self.cliente} para {self.servicio}"


class Encargado(models.Model):
    nombre = models.CharField(max_length=45)
    apellido = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    correo = models.CharField(max_length=45)
    telefono = models.CharField(max_length=9)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Servicios(models.Model):
    nombre_servicio = models.CharField(max_length=45)
    descripcion = models.CharField(max_length=100)
    precio = models.IntegerField()
    duracion = models.CharField(max_length=45)

    def __str__(self):
        return self.nombre_servicio


class Reviews(models.Model):
    comentarios = models.CharField(max_length=45)
    calificacion = models.CharField(max_length=45)
    fecha_review = models.DateField()
    cliente = models.ForeignKey('Clientes', on_delete=models.CASCADE, null=True )
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
