"""
urls.py

Definición de las rutas de URL para la aplicación Django. 
Cada entrada de la lista urlpatterns asocia una URL con una vista específica.

Imports:
    - path: Función para asociar URLs con vistas.
    - views: Módulo que contiene las vistas de la aplicación.
    - admin: Módulo para habilitar el panel de administración de Django.
"""

from django.urls import path
from app1 import views
from django.contrib import admin

# Lista de rutas URL con sus vistas correspondientes
urlpatterns = [
    # Ruta raíz que redirige a la vista principal de inicio.
    path('', views.home, name='index_redirect'),
    
    # Vista principal de la aplicación.
    path('home/', views.home, name='home'),
    
    # Vista del índice administrativo.
    path('index_admin/', views.index_admin, name='index_admin'),
    
    # Panel de administración de Django.
    path('admin/', admin.site.urls),
    
    # Vista del carrito de compras.
    path('carrito/', views.carrito, name='carrito'),
    
    # Ruta para cerrar sesión.
    path('logout/', views.logout_view, name='logout'),
    
    # Registro de nuevos clientes.
    path('register/', views.registrar_cliente, name='register'),
    
    # Gestión de reservas para los usuarios.
    path('reservas/', views.reservas_view, name='reservas'),
    
    # Formulario para agregar un nuevo vehículo.
    path('agregar_vehiculo/', views.agregar_vehiculo, name='agregar_vehiculo'),
    
    # Vista para listar los vehículos del cliente.
    path('ver_vehiculos/', views.ver_vehiculos, name='ver_vehiculos'),
    
    # Ruta para el inicio de sesión de usuarios.
    path('login/', views.login_view, name='login'), 
    
    # Vista administrativa para ver todos los clientes registrados.
    path('clientesadmin/', views.ver_clientes, name='ver_clientes_admin'),
    
    # Vista administrativa para ver todos los vehículos registrados.
    path('vehiculosadmin/', views.ver_vehiculos_admin, name='ver_vehiculos_admin'),
    
    # Vista administrativa para gestionar reservas.
    path('reservasadmin/', views.ver_reservas_admin, name='ver_reservas_admin'),
    
    # Vista para listar los vehículos de un cliente específico.
    path('clientes/<int:cliente_id>/vehiculos/', views.cliente_vehiculos, name='cliente_vehiculos'),
    
    # Vista de la página de visión de la empresa.
    path('vision/', views.vision_view, name='vision'),
    
    # Página sobre la historia y valores de la empresa.
    path('quienes-somos/', views.quienes_somos_view, name='quienes_somos'),
    
    # Vista de la página de misión de la empresa.
    path('mision/', views.mision_view, name='mision'),
    
    # Vista para listar las reseñas de los clientes.
    path('resenas/', views.ver_resenas_view, name='ver_resenas_view'),
    
    # Formulario para que los usuarios agreguen una reseña.
    path('agregar-resena/', views.agregar_resena_view, name='agregar_resena'),
    
    # Ruta para actualizar una reseña existente.
    path('actualizar_resena/<int:resena_id>/', views.actualizar_resena, name='actualizar_resena'),
    
    # Ruta para eliminar una reseña existente.
    path('eliminar_resena/<int:resena_id>/', views.eliminar_resena, name='eliminar_resena'),
]
