# models.py
from django.db import models
from django.contrib.auth.models import User

class Encargado(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=True)  # Relación con User para manejar credenciales
    nombre = models.CharField(max_length=45, null=True)
    apellido = models.CharField(max_length=45, null=True)
    telefono = models.CharField(max_length=45, null=True)
    correo = models.CharField(max_length=45, null=True)

    def __str__(self):
        return self.nombre or "Encargado sin nombre"


class Cliente(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=True)  # Relación con User para manejar credenciales
    nombre = models.CharField(max_length=45, null=True)
    telefono = models.CharField(max_length=45, null=True)
    direccion = models.CharField(max_length=45, null=True)
    correo = models.CharField(max_length=45, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    # arreglar el forms,views con encargado y cliente, reiniciar makemigrations
    def __str__(self):
        return self.nombre or "Cliente sin nombre"


class Vehiculo(models.Model):
    marca = models.CharField(max_length=45, null=True)
    modelo = models.CharField(max_length=45, null=True)
    year = models.CharField(max_length=45, null=True)
    patente = models.CharField(max_length=5, null=True)

    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.patente})"


class Servicio(models.Model):
    nombre = models.CharField(max_length=45, null=True)
    descripcion = models.CharField(max_length=100, null=True)
    precio = models.IntegerField(null=True)
    duracion = models.CharField(max_length=45, null=True)

    def __str__(self):
        return self.nombre


class Reserva(models.Model):
    hora_reserva = models.DateTimeField(null=True)
    fecha_reserva = models.DateTimeField(null=True)
    estado = models.CharField(max_length=20, null=True)
    administrador = models.ForeignKey(Encargado, on_delete=models.SET_NULL, null=True)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, null=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Reserva de {self.cliente.nombre} para {self.servicio.nombre}"


class Review(models.Model):
    comentarios = models.CharField(max_length=45, null=True)
    calificacion = models.IntegerField(null=True)
    fecha_review = models.DateField(null=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Review de {self.cliente.nombre} para {self.vehiculo.marca}"


