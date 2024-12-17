
from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password,check_password


# Modelo para representar a los encargados del sistema.
class Encargado(models.Model):
    nombre = models.CharField(max_length=45)  # Nombre del encargado.
    apellido = models.CharField(max_length=45)  # Apellido del encargado.
    password = models.CharField(max_length=300)  # Contraseña cifrada.
    correo = models.EmailField(max_length=45)  # Correo electrónico único del encargado.
    telefono = models.CharField(max_length=9)  # Teléfono de contacto.

    # Método para cifrar y guardar la contraseña.
    def set_password(self, password):
        self.password = make_password(password)

    # Representación legible del encargado.
    def __str__(self):
        return f"{self.nombre} {self.apellido}"


# Modelo para representar las reservas realizadas por los clientes.
class Reservas(models.Model):
    hora_reserva = models.DateTimeField()  # Fecha y hora específica de la reserva.
    fecha_reserva = models.DateTimeField()  # Fecha de creación o confirmación de la reserva.
    estado = models.CharField(max_length=20)  # Estado de la reserva (ejemplo: "pendiente", "confirmada").
    administrador = models.ForeignKey(
        'Encargado', on_delete=models.SET_NULL, null=True
    )  # Relación con el encargado que administra la reserva.
    servicios = models.ManyToManyField('Servicios')  # Servicios incluidos en la reserva.
    cliente = models.ForeignKey(
        'Clientes', on_delete=models.CASCADE, null=True
    )  # Cliente asociado a la reserva.
    vehiculo = models.ForeignKey(
        'Vehiculo', on_delete=models.CASCADE, null=True
    )  # Vehículo relacionado con la reserva.

    # Representación legible de la reserva.
    def __str__(self):
        return f"Reserva de {self.cliente} para {', '.join(s.nombre_servicio for s in self.servicios.all())}"


# Modelo para representar servicios ofrecidos.
class Servicios(models.Model):
    nombre_servicio = models.CharField(max_length=45)  # Nombre del servicio.
    descripcion = models.CharField(max_length=100)  # Breve descripción del servicio.
    precio = models.IntegerField()  # Precio del servicio.
    duracion = models.CharField(max_length=45)  # Duración del servicio (ejemplo: "30 minutos").

    # Representación legible del servicio.
    def __str__(self):
        return self.nombre_servicio


# Modelo para representar reseñas realizadas por los clientes.
class Reviews(models.Model):
    comentarios = models.CharField(max_length=45)  # Comentarios sobre el servicio o vehículo.
    calificacion = models.IntegerField()  # Calificación del servicio, entre 1 y 5.
    fecha_review = models.DateField()  # Fecha en que se realizó la reseña.
    cliente = models.ForeignKey(
        'Clientes', on_delete=models.CASCADE, null=True
    )  # Cliente que hizo la reseña.
    vehiculo = models.ForeignKey(
        'Vehiculo', on_delete=models.CASCADE, null=True
    )  # Vehículo relacionado con la reseña.

    # Representación legible de la reseña.
    def __str__(self):
        return f"Review de {self.cliente} para {self.vehiculo}"


# Modelo para representar a los clientes.
class Clientes(models.Model):
    nombre = models.CharField(max_length=45)  # Nombre del cliente.
    email = models.EmailField(max_length=45)  # Correo electrónico único del cliente.
    password = models.CharField(max_length=300)  # Contraseña cifrada del cliente.
    telefono = models.CharField(max_length=45)  # Teléfono de contacto.
    direccion = models.CharField(max_length=45)  # Dirección del cliente.
    fecha_registro = models.DateTimeField(default=timezone.now, null=True)  # Fecha de registro del cliente.

    # Método para cifrar y guardar la contraseña.
    def set_password(self, password):
        self.password = make_password(password)
    
    def check_password(self, password):
        return check_password(password, self.password)

    # Representación legible del cliente.
    def __str__(self):
        return self.nombre


# Modelo para representar vehículos asociados a los clientes.
class Vehiculo(models.Model):
    cliente = models.ForeignKey(
        Clientes, on_delete=models.CASCADE, related_name="vehiculos", null=True
    )  # Relación de "uno a muchos" con los clientes.
    marca = models.CharField(max_length=45)  # Marca del vehículo.
    modelo = models.CharField(max_length=45)  # Modelo del vehículo.
    year = models.CharField(max_length=45)  # Año de fabricación del vehículo.
    patente = models.CharField(max_length=5)  # Patente o matrícula del vehículo.

    # Representación legible del vehículo.
    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.patente})"
