from django.urls import path
from app1 import views

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("home/", views.home, name="home"),
    path("admin/", views.index_admin, name="index_admin"),
    # Otras rutas según la estructura de tu aplicación
]
