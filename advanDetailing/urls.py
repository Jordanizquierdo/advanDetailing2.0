# urls.py
from django.urls import path
from app1 import views
from django.contrib import admin

urlpatterns = [
    path('', views.home),
    path('admin/', admin.site.urls),
    # path('service/<str:service>', views.service_detail, name='service_detail'),
    # path('users', views.user_list, name='user_list'),
    path('carrito/',views.carrito)
]
