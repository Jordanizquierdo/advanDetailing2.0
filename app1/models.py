from django.db import models

class Clientes(models.Model):
    nombre = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    telefono = models.CharField(max_length=45)
    direccion = models.CharField(max_length=45)
    fecha_registro = models.DateTimeField()
    vehiculo_id = models.IntegerField()


class Reservas(models.Model):
    hora_Reserva = models.DateTimeField()
    fecha_Reserva = models.DateField()
    estado = models.CharField(max_length=20)
    administrador_id = models.IntegerField()
    servicio_id = models.IntegerField()
    clientes_id = models.IntegerField()
    clientes_id_vehiculo = models.IntegerField()


class Encargado(models.Model):
    nombre = models.CharField(max_length=45)
    apellido = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    correo = models.CharField(max_length=45)
    telefono = models.CharField(max_length=9)


class Servicios(models.Model):
    nombre_servicio = models.CharField(max_length=45)
    descripcion = models.CharField(max_length=100)
    precio = models.IntegerField()
    duracion = models.CharField(max_length=45)


class Reviews(models.Model):
    comentarios = models.CharField(max_length=45)
    calificacion = models.CharField(max_length=45)
    fecha_review = models.DateField()
    clientes_id = models.IntegerField()
    clientes_id_vehiculo = models.IntegerField()

class Vehiculo(models.Model):
    marca = models.CharField(max_length=45)
    modelo = models.CharField(max_length=45)
    year = models.CharField(max_length=45)
    patente = models.CharField(max_length=5)