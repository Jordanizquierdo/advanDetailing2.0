# admin.py
from django.contrib import admin
from .models import Encargado, Cliente, Vehiculo, Servicio, Reserva, Review

@admin.register(Encargado)
class EncargadoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'telefono', 'correo', 'usuario')
    search_fields = ('nombre', 'telefono', 'correo')

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'telefono', 'direccion', 'usuario')
    search_fields = ('nombre', 'telefono', 'direccion')

@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ('marca', 'modelo', 'year', 'patente')
    search_fields = ('marca', 'modelo', 'patente')

@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'precio', 'duracion')
    search_fields = ('nombre', 'descripcion')
    list_filter = ('precio',)

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('hora_reserva', 'fecha_reserva', 'estado', 'administrador', 'servicio', 'cliente', 'vehiculo')
    search_fields = ('estado',)
    list_filter = ('estado', 'fecha_reserva')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('comentarios', 'calificacion', 'fecha_review', 'cliente', 'vehiculo')
    search_fields = ('comentarios',)
    list_filter = ('calificacion', 'fecha_review')
