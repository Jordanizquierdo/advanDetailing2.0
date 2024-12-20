from django.contrib import admin
from django.contrib.auth.hashers import make_password  # Importa make_password
from .models import Clientes, Reservas, Encargado, Servicios, Reviews, Vehiculo

"""
Configuración del panel de administración de Django para la gestión de modelos.

Este archivo registra y configura modelos para su gestión en el panel de administración de Django. 
Se implementan funciones personalizadas para mejorar la experiencia de administración, como 
mostrar vehículos asociados y servicios relacionados, así como cifrar contraseñas de usuarios 
antes de guardarlos en la base de datos.

Modelos Registrados:
--------------------
1. **Clientes**: Permite gestionar la información de los clientes, con soporte para cifrado de 
   contraseñas y visualización de vehículos asociados.
   
2. **Reservas**: Administra reservas, mostrando detalles del cliente, vehículo y servicios relacionados.

3. **Encargado**: Gestiona datos de los encargados, incluyendo cifrado de contraseñas.

4. **Servicios**: Muestra servicios ofrecidos con información detallada.

5. **Reviews**: Permite gestionar reseñas realizadas por los clientes.

6. **Vehiculo**: Administra vehículos registrados, mostrando detalles clave como marca, modelo y patente.

Funciones Personalizadas:
-------------------------
- **mostrar_vehiculos**: Lista los vehículos asociados a un cliente en el panel de administración.
- **mostrar_servicios**: Lista los servicios asociados a una reserva específica.
- **save_model**: Cifra las contraseñas antes de guardar objetos de los modelos `Clientes` y `Encargado`.

Notas Importantes:
------------------
- `make_password` se utiliza para asegurar el almacenamiento seguro de contraseñas.
- `list_display` define los campos que se muestran en la lista principal de cada modelo.
- Se añaden descripciones amigables usando `short_description` para mejorar la presentación en la interfaz de administración.
"""

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
