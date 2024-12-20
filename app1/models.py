from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password


class Encargado(models.Model):
    """
    Modelo que representa a los encargados del sistema.

    Atributos:
        nombre (str): Nombre del encargado.
        apellido (str): Apellido del encargado.
        password (str): Contraseña cifrada del encargado.
        correo (EmailField): Correo electrónico único del encargado.
        telefono (str): Teléfono de contacto.

    Métodos:
        set_password(password): Cifra y guarda la contraseña.
        __str__(): Retorna una representación legible del encargado.
    """
    nombre = models.CharField(max_length=45)  
    apellido = models.CharField(max_length=45)
    password = models.CharField(max_length=300)
    correo = models.EmailField(max_length=45, unique=True)
    telefono = models.CharField(max_length=9)

    def set_password(self, password):
        """
        Cifra la contraseña proporcionada y la guarda en el modelo.

        Args:
            password (str): Contraseña en texto plano.
        """
        self.password = make_password(password)

    def __str__(self):
        """
        Retorna una representación legible del encargado.

        Returns:
            str: Nombre y apellido del encargado.
        """
        return f"{self.nombre} {self.apellido}"


class Reservas(models.Model):
    """
    Modelo que representa las reservas realizadas por los clientes.

    Atributos:
        hora_reserva (DateTime): Fecha y hora específica de la reserva.
        fecha_reserva (DateTime): Fecha de creación o confirmación de la reserva.
        estado (str): Estado actual de la reserva.
        administrador (ForeignKey): Encargado que administra la reserva.
        servicios (ManyToManyField): Servicios incluidos en la reserva.
        cliente (ForeignKey): Cliente asociado a la reserva.
        vehiculo (ForeignKey): Vehículo relacionado con la reserva.

    Métodos:
        __str__(): Retorna una representación legible de la reserva.
    """
    hora_reserva = models.DateTimeField()  
    fecha_reserva = models.DateTimeField()  
    estado = models.CharField(max_length=20) 
    administrador = models.ForeignKey(
        'Encargado', on_delete=models.SET_NULL, null=True
    )
    servicios = models.ManyToManyField('Servicios')  
    cliente = models.ForeignKey(
        'Clientes', on_delete=models.CASCADE, null=True
    )
    vehiculo = models.ForeignKey(
        'Vehiculo', on_delete=models.CASCADE, null=True
    )

    def __str__(self):
        """
        Retorna una representación legible de la reserva.

        Returns:
            str: Descripción de la reserva.
        """
        servicios_nombres = ', '.join(s.nombre_servicio for s in self.servicios.all())
        return f"Reserva de {self.cliente} para {servicios_nombres}"


class Servicios(models.Model):
    """
    Modelo que representa los servicios ofrecidos por el sistema.

    Atributos:
        nombre_servicio (str): Nombre del servicio.
        descripcion (str): Breve descripción del servicio.
        precio (int): Precio del servicio.
        duracion (str): Duración estimada del servicio.

    Métodos:
        __str__(): Retorna una representación legible del servicio.
    """
    nombre_servicio = models.CharField(max_length=45)  
    descripcion = models.CharField(max_length=100) 
    precio = models.IntegerField()
    duracion = models.CharField(max_length=45)

    def __str__(self):
        """
        Retorna una representación legible del servicio.

        Returns:
            str: Nombre del servicio.
        """
        return self.nombre_servicio


class Reviews(models.Model):
    """
    Modelo que representa las reseñas de clientes sobre vehículos.

    Atributos:
        comentarios (str): Comentarios del cliente sobre el servicio o vehículo.
        calificacion (int): Calificación entre 1 y 5.
        fecha_review (Date): Fecha de creación de la reseña.
        cliente (ForeignKey): Cliente que hizo la reseña.
        vehiculo (ForeignKey): Vehículo relacionado con la reseña.

    Métodos:
        __str__(): Retorna una representación legible de la reseña.
    """
    comentarios = models.CharField(max_length=45)  
    calificacion = models.IntegerField()
    fecha_review = models.DateField()
    cliente = models.ForeignKey(
        'Clientes', on_delete=models.CASCADE, null=True
    )
    vehiculo = models.ForeignKey(
        'Vehiculo', on_delete=models.CASCADE, null=True
    )

    def __str__(self):
        """
        Retorna una representación legible de la reseña.

        Returns:
            str: Descripción de la reseña.
        """
        return f"Review de {self.cliente} para {self.vehiculo}"


class Clientes(models.Model):
    """
    Modelo que representa a los clientes registrados en el sistema.

    Atributos:
        nombre (str): Nombre del cliente.
        email (EmailField): Correo electrónico único del cliente.
        password (str): Contraseña cifrada.
        telefono (str): Teléfono de contacto.
        direccion (str): Dirección del cliente.
        fecha_registro (DateTime): Fecha de registro del cliente.

    Métodos:
        set_password(password): Cifra y guarda la contraseña.
        check_password(password): Comprueba si una contraseña coincide con la cifrada.
        __str__(): Retorna una representación legible del cliente.
    """
    nombre = models.CharField(max_length=45)
    email = models.EmailField(max_length=45, unique=True)
    password = models.CharField(max_length=300)
    telefono = models.CharField(max_length=45)
    direccion = models.CharField(max_length=45)
    fecha_registro = models.DateTimeField(default=timezone.now, null=True)

    def set_password(self, password):
        self.password = make_password(password)

    def check_password(self, password):
        return check_password(password, self.password)

    def __str__(self):
        return self.nombre


class Vehiculo(models.Model):
    """
    Modelo que representa los vehículos pertenecientes a un cliente.

    Atributos:
        cliente (ForeignKey): Cliente propietario del vehículo.
        marca (str): Marca del vehículo.
        modelo (str): Modelo del vehículo.
        year (str): Año de fabricación del vehículo.
        patente (str): Patente o matrícula del vehículo.

    Métodos:
        __str__(): Retorna una representación legible del vehículo.
    """
    cliente = models.ForeignKey(
        Clientes, on_delete=models.CASCADE, related_name="vehiculos", null=True
    )
    marca = models.CharField(max_length=45)
    modelo = models.CharField(max_length=45)
    year = models.CharField(max_length=45)
    patente = models.CharField(max_length=5)

    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.patente})"



class ErrorLog(models.Model):
    """
    Modelo que almacena registros de errores del sistema.

    Atributos:
        timestamp (DateTime): Fecha y hora en que ocurrió el error.
        error_type (str): Tipo o nivel del error (ej: ERROR, WARNING).
        error_message (str): Mensaje descriptivo del error.
        stack_trace (str): Trazas de error detalladas.

    Métodos:
        __str__(): Retorna una representación legible del log de error.
    """
    timestamp = models.DateTimeField(auto_now_add=True)
    error_type = models.CharField(max_length=255)
    error_message = models.TextField()
    stack_trace = models.TextField()

    def __str__(self):
        """
        Retorna una representación legible del registro de error.

        Returns:
            str: Tipo de error y la fecha del registro.
        """
        return f"{self.error_type} - {self.timestamp}"
