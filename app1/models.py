from django.db import models

# Modelo para representar las marcas de vehículos.
class Marca(models.Model):
    id_marca = models.AutoField(primary_key=True)
    marca = models.CharField(max_length=50)

    def __str__(self):
        return self.marca


# Modelo para representar los modelos de vehículos.
class Modelo(models.Model):
    id_modelo = models.AutoField(primary_key=True)
    id_marca = models.ForeignKey(
        Marca, on_delete=models.CASCADE, related_name="modelos", null=True, blank=True
    )
    modelo = models.CharField(max_length=50)

    def __str__(self):
        return self.modelo


# Modelo para representar los clientes.
class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=300)
    telefono = models.CharField(max_length=15)
    direccion = models.CharField(max_length=100)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def set_password(self, password):
        from django.contrib.auth.hashers import make_password
        self.password = make_password(password)

    def __str__(self):
        return self.nombre


# Modelo para representar los vehículos de los clientes.
class Vehiculo(models.Model):
    id_vehiculo = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey(
        Cliente, on_delete=models.CASCADE, related_name="vehiculos", null=True, blank=True
    )
    id_modelo = models.ForeignKey(
        Modelo, on_delete=models.CASCADE, null=True, blank=True
    )
    id_marca = models.ForeignKey(
        Marca, on_delete=models.CASCADE, null=True, blank=True
    )
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    year = models.CharField(max_length=4)
    patente = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.patente})"


# Modelo para representar los encargados.
class Encargado(models.Model):
    id_encargado = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    password = models.CharField(max_length=300)
    correo = models.EmailField(unique=True)

    def set_password(self, password):
        from django.contrib.auth.hashers import make_password
        self.password = make_password(password)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


# Modelo para representar los servicios ofrecidos.
class Servicios(models.Model):
    id_servicio = models.AutoField(primary_key=True)
    nombre_servicio = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    duracion = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre_servicio


# Modelo para representar las reservas realizadas.
class Reservas(models.Model):
    id_reserva = models.AutoField(primary_key=True)
    id_encargado = models.ForeignKey(
        Encargado, on_delete=models.SET_NULL, null=True, blank=True
    )
    id_vehiculo = models.ForeignKey(
        Vehiculo, on_delete=models.CASCADE, null=True, blank=True
    )
    hora_reserva = models.DateTimeField()
    fecha_reserva = models.DateTimeField()
    estado = models.CharField(max_length=20)

    def __str__(self):
        return f"Reserva {self.id_reserva} - Estado: {self.estado}"


# Modelo intermedio para representar los servicios en una reserva.
class ReservasServicios(models.Model):
    id_servicio = models.ForeignKey(
        Servicios, on_delete=models.CASCADE, null=True, blank=True
    )
    id_reserva = models.ForeignKey(
        Reservas, on_delete=models.CASCADE, null=True, blank=True
    )
    metodo_de_pago = models.CharField(max_length=50)

    def __str__(self):
        return f"Servicio {self.id_servicio} en Reserva {self.id_reserva}"


# Modelo para representar las reseñas de clientes.
class Reviews(models.Model):
    id_review = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey(
        Cliente, on_delete=models.CASCADE, null=True, blank=True
    )
    comentarios = models.CharField(max_length=255)
    calificacion = models.IntegerField()
    fecha_review = models.DateField()

    def __str__(self):
        return f"Review {self.id_review} - Calificación: {self.calificacion}"
