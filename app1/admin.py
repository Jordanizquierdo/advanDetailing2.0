from django.contrib import admin
from django.contrib.auth.hashers import make_password  # Importa make_password
from .models import Clientes, Reservas, Encargado, Servicios, Reviews, Vehiculo

# Registro para el modelo Clientes
@admin.register(Clientes)
class ClientesAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'email', 'telefono', 'direccion', 'fecha_registro', 'mostrar_vehiculos')

    def save_model(self, request, obj, form, change):
        # Si la contraseña ha cambiado o se está creando un nuevo cliente
        if obj.password:
            obj.password = make_password(obj.password)  # Cifra la contraseña antes de guardarla
        super().save_model(request, obj, form, change)

    def mostrar_vehiculos(self, obj):
        # Accede a los vehículos del cliente utilizando la relación ManyToManyField
        return ", ".join([vehiculo.marca for vehiculo in obj.vehiculos.all()])  # Usa obj.vehiculos en lugar de obj.vehiculo

    mostrar_vehiculos.short_description = 'Vehículos'  # Título de la columna en el admin

# Registro para el modelo Reservas
@admin.register(Reservas)
class ReservasAdmin(admin.ModelAdmin):
    list_display = ('id', 'hora_reserva', 'fecha_reserva', 'estado', 'administrador', 'mostrar_servicios', 'cliente', 'vehiculo')

    def mostrar_servicios(self, obj):
        # Muestra los nombres de los servicios relacionados con esta reserva
        return ", ".join([servicio.nombre_servicio for servicio in obj.servicios.all()])

    mostrar_servicios.short_description = 'Servicios'  # Título de la columna en el admin

# Registro para el modelo Encargado
@admin.register(Encargado)
class EncargadoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'apellido', 'correo', 'telefono')

    def save_model(self, request, obj, form, change):
        # Si la contraseña ha cambiado o se está creando un nuevo encargado
        if obj.password:
            obj.password = make_password(obj.password)  # Cifra la contraseña antes de guardarla
        super().save_model(request, obj, form, change)

# Registro para el modelo Servicios
@admin.register(Servicios)
class ServiciosAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_servicio', 'descripcion', 'precio', 'duracion')

# Registro para el modelo Reviews
@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'comentarios', 'calificacion', 'fecha_review', 'cliente', 'vehiculo')

# Registro para el modelo Vehiculo
@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ('id', 'marca', 'modelo', 'year', 'patente')
