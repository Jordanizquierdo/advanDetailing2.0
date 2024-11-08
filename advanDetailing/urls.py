# urls.py
from django.urls import path
from app1 import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('registro/', views.registrar, name='registro'),
]
