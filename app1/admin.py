from django.contrib import admin
from django.contrib.auth.hashers import make_password  # Importa make_password
from .models import Clientes, Reservas, Encargado, Servicios, Reviews, Vehiculo

@admin.register(Clientes)
class ClientesAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'email', 'telefono', 'direccion', 'fecha_registro', 'vehiculo')

    def save_model(self, request, obj, form, change):
        # Si la contraseña ha cambiado o se está creando un nuevo cliente
        if obj.password:
            obj.password = make_password(obj.password)  # Cifra la contraseña antes de guardarla
        super().save_model(request, obj, form, change)

@admin.register(Reservas)
class ReservasAdmin(admin.ModelAdmin):
    list_display = ('id', 'hora_reserva', 'fecha_reserva', 'estado', 'administrador', 'servicio', 'cliente', 'vehiculo')

@admin.register(Encargado)
class EncargadoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'apellido', 'correo', 'telefono')

    def save_model(self, request, obj, form, change):
        # Si la contraseña ha cambiado o se está creando un nuevo encargado
        if obj.password:
            obj.password = make_password(obj.password)  # Cifra la contraseña antes de guardarla
        super().save_model(request, obj, form, change)

@admin.register(Servicios)
class ServiciosAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_servicio', 'descripcion', 'precio', 'duracion')

@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'comentarios', 'calificacion', 'fecha_review', 'cliente', 'vehiculo')

@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ('id', 'marca', 'modelo', 'year', 'patente')
