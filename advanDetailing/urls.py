# urls.py
from django.urls import path
from app1 import views
from django.contrib import admin

urlpatterns = [
    path('', views.home, name='index_redirect'),
    path('home/', views.home, name='home'),
    path('index_admin/', views.index_admin, name='index_admin'),
    path('admin/', admin.site.urls),
    path('carrito/', views.carrito, name='carrito'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.registrar_cliente, name='register'),
    path('reservas/', views.reservas_view, name='reservas'),
    path('agregar_vehiculo/', views.agregar_vehiculo, name='agregar_vehiculo'),
    path('ver_vehiculos/', views.ver_vehiculos, name='ver_vehiculos'),
    path('login/', views.login_view, name='login'), 
    path('clientesadmin/', views.ver_clientes, name='ver_clientes_admin'),
    path('vehiculosadmin/', views.ver_vehiculos_admin, name='ver_vehiculos_admin'),
    path('reservasadmin/', views.ver_reservas, name='ver_reservas_admin'),
    path('clientes/<int:cliente_id>/vehiculos/', views.cliente_vehiculos, name='cliente_vehiculos'),
    path('vision/', views.vision_view, name='vision'),
    path('quienes-somos/', views.quienes_somos_view, name='quienes_somos'),
    path('mision/', views.mision_view, name='mision'),
    path('resenas/', views.ver_resenas_view, name='ver_resenas'),
    path('agregar-resena/', views.agregar_resena_view, name='agregar_resena'),
    path('actualizar_resena/<int:resena_id>/', views.actualizar_resena, name='actualizar_resena'),
    path('eliminar_resena/<int:resena_id>/', views.eliminar_resena, name='eliminar_resena')


]