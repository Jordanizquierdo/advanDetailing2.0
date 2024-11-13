# urls.py
from django.urls import path
from app1 import views
from django.contrib import admin

urlpatterns = [
    path('', views.login_view, name='login'), 
    path('home/', views.home, name='home'),
    path('index_admin/', views.index_admin, name='index_admin'),
    path('admin/', admin.site.urls),
    path('carrito/', views.carrito, name='carrito'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.registrar_cliente, name='register'),
]
