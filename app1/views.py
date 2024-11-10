from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Clientes, Encargado
from .forms import CustomAuthenticationForm

def login_view(request):
    """Vista de inicio de sesión usando autenticación de Django."""
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect("index_admin")
        else:
            return redirect("/home")

    form = CustomAuthenticationForm()

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_cliente:
                return redirect("/home")
            elif user.is_encargado:
                return redirect("index_admin")
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")

    return render(request, "app1/login.html", {"form": form})

def logout_view(request):
    """Cierra la sesión y redirige al login."""
    logout(request)
    return redirect('login')

def home(request):
    """Renderiza el home con datos del carrito."""
    cart = request.session.get('cart', [])
    total = sum(item['price'] for item in cart)
    data = {'cart': cart, 'total': total}
    return render(request, 'app1/index_user.html', data)

def index_admin(request):
    """Renderiza la vista del administrador."""
    return render(request, 'app1/index_admin.html')
