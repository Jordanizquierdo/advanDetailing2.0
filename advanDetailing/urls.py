# urls.py
from django.urls import path
from app1 import views

urlpatterns = [
    path('', views.home, name='home'),
    # path('service/<str:service>', views.service_detail, name='service_detail'),
    # path('users', views.user_list, name='user_list'),
]
