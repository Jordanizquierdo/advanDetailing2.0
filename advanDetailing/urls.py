from django.urls import path
from app1.views import (
    CustomLoginView, home, carrito, agregar_al_carrito, eliminar_del_carrito,
    logout_view, index_admin
)
from app1 import views
from django.contrib import admin

urlpatterns = [
    path('', CustomLoginView.as_view(), name='login'),  # Vista de login
    path('logout/', logout_view, name='logout'),               # Vista de logout
    path('home/', home, name='home'),                          # Página principal para clientes
    path('admin1/', index_admin, name='index_admin'),           # Página de administración
    path('carrito/', carrito, name='carrito'),                 # Página del carrito
    path('agregar/<int:servicio_id>/', agregar_al_carrito, name='agregar_al_carrito'),  # Agregar al carrito
    path('eliminar/<int:servicio_id>/', eliminar_del_carrito, name='eliminar_del_carrito'),  # Eliminar del carrito
    # path('', views.login, name='redirect_to_login'),     # Redirección inicial
    path('register/',views.register_view, name='register'),
    path('admin/', admin.site.urls),
]
