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
        password = password.strip() 


        # cliente
        if email and password:
            try:
                cliente = Clientes.objects.get(email__iexact=email)
                if check_password(password, cliente.password): 
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
                if check_password(password, encargado.password):  
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
    cliente_id = request.session.get('cliente_id')
    cart = request.session.get('cart', [])
    total = sum(item['price'] for item in cart)
    data = {'cart': cart, 'total': total,"cliente_id": cliente_id}
    return render(request, 'app1/index_user.html', data)

def index_admin(request):
    

    return render(request, 'app1/index_admin.html')





from datetime import datetime
from django.shortcuts import render, redirect
from .models import Reservas, Servicios

from django.shortcuts import render, redirect
from .models import Reservas, Servicios, Vehiculo
from datetime import datetime
import json

def carrito(request):
    # Obtener los datos del carrito y cliente desde la URL
    cliente_id = request.GET.get('clienteId')
    cart_data = request.GET.get("cartList", "[]")
    try:
        cart_data = json.loads(cart_data)
        cliente_id = int(cliente_id)
    except json.JSONDecodeError:
        cart_data = []

    total = sum(item['price'] for item in cart_data)
    context = {'cart_items': cart_data, 'total': total, 'cliente_id': cliente_id}

    # Obtener los vehículos del cliente para el formulario
    try:
        cliente = Clientes.objects.get(id=cliente_id)
        vehiculos = cliente.vehiculos.all()  # Obtiene todos los vehículos del cliente
    except Clientes.DoesNotExist:
        context['error'] = "Cliente no encontrado."
        return render(request, 'app1/carrito.html', context)

    context['vehiculos'] = vehiculos

    # Si la solicitud es POST, guarda la reserva
    if request.method == 'POST':
        # Obtener datos de fecha, hora y vehículo desde el formulario
        fecha_reserva = request.POST.get('fecha_reserva')
        hora_reserva = request.POST.get('hora_reserva')
        vehiculo_id = request.POST.get('vehiculo')  # ID del vehículo seleccionado
        estado = "pendiente"  # Estado inicial de la reserva

        # Combina fecha y hora en un solo campo de DateTimeField
        try:
            fecha_hora_reserva = datetime.strptime(f"{fecha_reserva} {hora_reserva}", "%Y-%m-%d %H:%M")
        except ValueError:
            context['error'] = "Fecha y hora no válidas."
            return render(request, 'app1/carrito.html', context)

        # Obtener el vehículo seleccionado
        try:
            vehiculo = Vehiculo.objects.get(id=vehiculo_id)
        except Vehiculo.DoesNotExist:
            context['error'] = "Vehículo no válido."
            return render(request, 'app1/carrito.html', context)

        # Crear y guardar la nueva reserva
        reserva = Reservas(
            hora_reserva=fecha_hora_reserva,
            fecha_reserva=fecha_hora_reserva,
            estado=estado,
            cliente=cliente,  
            vehiculo=vehiculo, 
        )
        reserva.save()

        # Asocia los servicios seleccionados a la reserva
        for item in cart_data:
            servicio = Servicios.objects.get(id=item['id'])
            reserva.servicios.add(servicio)


        return redirect('home')  # Redirige a la página principal

    return render(request, 'app1/carrito.html', context)


