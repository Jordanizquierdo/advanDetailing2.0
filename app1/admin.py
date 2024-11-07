from django.contrib import admin
from .models import Clientes, Reservas, Encargado, Servicios, Reviews, Vehiculo

@admin.register(Clientes)
class ClientesAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'email', 'telefono', 'direccion', 'fecha_registro', 'vehiculo_id')

@admin.register(Reservas)
class ReservasAdmin(admin.ModelAdmin):
    list_display = ('id', 'hora_Reserva', 'fecha_Reserva', 'estado', 'administrador_id', 'servicio_id', 'clientes_id', 'clientes_id_vehiculo')

@admin.register(Encargado)
class EncargadoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'apellido', 'correo', 'telefono')

@admin.register(Servicios)
class ServiciosAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_servicio', 'descripcion', 'precio', 'duracion')

@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'comentarios', 'calificacion', 'fecha_review', 'clientes_id', 'clientes_id_vehiculo')

@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ('id', 'marca', 'modelo', 'year', 'patente')
