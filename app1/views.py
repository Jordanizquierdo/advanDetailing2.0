import json
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Clientes,Encargado
from .forms import CustomAuthenticationForm

from django.contrib.auth.hashers import check_password  # Importa check_password
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Clientes, Encargado
from .forms import CustomAuthenticationForm

def login_view(request):

    form = CustomAuthenticationForm()

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        correo = request.POST.get("email")
        password = password.strip()  # Elimina espacios al principio y al final de la contraseña


        # cliente
        if email and password:
            try:
                cliente = Clientes.objects.get(email__iexact=email)
                if check_password(password, cliente.password):  # Verifica la contraseña cifrada
                    request.session['cliente_id'] = cliente.id
                    print("Contraseña correcta")
                    return redirect("/home")
                else:
                    print("Contraseña incorrecta.")
                    print("html",password)
                    print("db",cliente.password)
                    messages.error(request, "Contraseña incorrecta.")
            except Clientes.DoesNotExist:
                messages.error(request, "No se encontró una cuenta con este correo.")

        # encargado
        if correo and password:
            try:
                encargado = Encargado.objects.get(correo__iexact=correo)
                if check_password(password, encargado.password):  # Verifica la contraseña cifrada
                    request.session['encargado_id'] = encargado.id
                    print("Contraseña correcta")
                    return redirect("index_admin")
                else:
                    print("Contraseña incorrecta.")
                    messages.error(request, "Contraseña incorrecta.")
            except Encargado.DoesNotExist:
                messages.error(request, "No se encontró una cuenta con este correo.")

    return render(request, "app1/login.html", {"form": form})


def logout_view(request):
    # Elimina la sesión y redirige al login
    request.session.flush()
    return redirect('login')

def home(request):
    # Renderiza el home con datos del carrito
    cart = request.session.get('cart', [])
    total = sum(item['price'] for item in cart)
    data = {'cart': cart, 'total': total}
    return render(request, 'app1/index_user.html', data)

def index_admin(request):
    

    return render(request, 'app1/index_admin.html')

def carrito(request):
    # Procesa el carrito y envía datos al template
    cart_data = request.GET.get("cartList", "[]")
    try:
        cart_data = json.loads(cart_data)
    except json.JSONDecodeError:
        cart_data = []
    total = sum(item['price'] for item in cart_data)
    context = {'cart_items': cart_data, 'total': total}
    return render(request, 'app1/carrito.html', context)
