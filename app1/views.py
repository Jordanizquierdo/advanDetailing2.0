import json
from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.utils.timezone import now
from .models import Clientes, Encargado, Reservas, Servicios, Vehiculo
from .forms import CustomAuthenticationForm, ClienteForm, VehiculoFormSet


def login_view(request):
    form = CustomAuthenticationForm()

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password").strip()

        # Autenticación del cliente
        if email and password:
            try:
                cliente = Clientes.objects.get(email__iexact=email)
                if check_password(password, cliente.password):
                    request.session['cliente_id'] = cliente.id
                    return redirect("/home")
                else:
                    messages.error(request, "Contraseña incorrecta.")
            except Clientes.DoesNotExist:
                messages.error(request, "No se encontró una cuenta con este correo.")

        # Autenticación del encargado
        if email and password:
            try:
                encargado = Encargado.objects.get(correo__iexact=email)
                if check_password(password, encargado.password):
                    request.session['encargado_id'] = encargado.id
                    return redirect("index_admin")
                else:
                    messages.error(request, "Contraseña incorrecta.")
            except Encargado.DoesNotExist:
                messages.error(request, "No se encontró una cuenta con este correo.")

    return render(request, "app1/login.html", {"form": form})


def logout_view(request):
    request.session.flush()
    return redirect('home')


def home(request):
    cliente_id = request.session.get('cliente_id')
    cliente = None
    if cliente_id:
        try:
            cliente = Clientes.objects.get(id=cliente_id)
        except Clientes.DoesNotExist:
            pass

    cart = request.session.get('cart', [])
    total = sum(item['price'] for item in cart)
    data = {
        'cart': cart,
        'total': total,
        'cliente_id': cliente_id,
        'cliente': cliente,
    }
    return render(request, 'app1/index_user.html', data)


def index_admin(request):
    print ("encargado_id")
    return render(request, 'app1/index_admin.html')


def carrito(request):
    cliente_id = request.session.get('cliente_id')
    if not cliente_id:
        messages.error(request, "Debes iniciar sesión para pagar.")
        return redirect('login')

    cart_data = request.GET.get("cartList", "[]")
    try:
        cart_data = json.loads(cart_data)
    except json.JSONDecodeError:
        cart_data = []

    total = sum(item['price'] for item in cart_data)
    context = {'cart_items': cart_data, 'total': total}

    try:
        cliente = Clientes.objects.get(id=cliente_id)
        vehiculos = cliente.vehiculos.all()
        context['vehiculos'] = vehiculos
    except Clientes.DoesNotExist:
        context['error'] = "Cliente no encontrado."
        return render(request, 'app1/carrito.html', context)

    if request.method == 'POST':
        fecha_reserva = request.POST.get('fecha_reserva')
        hora_reserva = request.POST.get('hora_reserva')
        vehiculo_id = request.POST.get('vehiculo')
        estado = "pendiente"

        try:
            fecha_hora_reserva = datetime.strptime(f"{fecha_reserva} {hora_reserva}", "%Y-%m-%d %H:%M")
        except ValueError:
            context['error'] = "Fecha y hora no válidas."
            return render(request, 'app1/carrito.html', context)

        try:
            vehiculo = Vehiculo.objects.get(id=vehiculo_id)
        except Vehiculo.DoesNotExist:
            context['error'] = "Vehículo no válido."
            return render(request, 'app1/carrito.html', context)

        reserva = Reservas(
            hora_reserva=fecha_hora_reserva,
            fecha_reserva=fecha_hora_reserva,
            estado=estado,
            cliente=cliente,
            vehiculo=vehiculo,
        )
        reserva.save()

        for item in cart_data:
            servicio = Servicios.objects.get(id=item['id'])
            reserva.servicios.add(servicio)

        return redirect('home')

    return render(request, 'app1/carrito.html', context)


def registrar_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        formset = VehiculoFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            cliente = form.save()
            vehiculos = formset.save(commit=False)
            for vehiculo in vehiculos:
                vehiculo.cliente = cliente
                vehiculo.save()
            return redirect('/')
    else:
        form = ClienteForm()
        formset = VehiculoFormSet()

    return render(request, 'app1/Registro.html', {'form': form, 'formset': formset})


def reservas_view(request):
    cliente_id = request.session.get('cliente_id')
    if not cliente_id:
        return redirect('login')

    try:
        cliente = Clientes.objects.get(id=cliente_id)
        reservas_futuras = Reservas.objects.filter(
            cliente=cliente,
            hora_reserva__gte=now()
        ).select_related('vehiculo').prefetch_related('servicios')

        reservas_pasadas = Reservas.objects.filter(
            cliente=cliente,
            hora_reserva__lt=now()
        ).select_related('vehiculo').prefetch_related('servicios')
    except Clientes.DoesNotExist:
        reservas_futuras = []
        reservas_pasadas = []
        cliente = None

    context = {
        'reservas_futuras': reservas_futuras,
        'reservas_pasadas': reservas_pasadas,
        'cliente': cliente,
    }
    return render(request, 'app1/reservas.html', context)


def agregar_vehiculo(request):
    cliente_id = request.session.get('cliente_id')
    if not cliente_id:
        return redirect('login')

    if request.method == 'POST':
        marca = request.POST.get('marca')
        modelo = request.POST.get('modelo')
        year = request.POST.get('year')
        patente = request.POST.get('patente')

        cliente = Clientes.objects.get(id=cliente_id)
        Vehiculo.objects.create(
            cliente=cliente,
            marca=marca,
            modelo=modelo,
            year=year,
            patente=patente
        )
        return redirect('ver_vehiculos')

    return render(request, 'app1/agregar_vehiculo.html')


def ver_vehiculos(request):
    cliente_id = request.session.get('cliente_id')
    if not cliente_id:
        return redirect('login')

    cliente = Clientes.objects.get(id=cliente_id)
    vehiculos = cliente.vehiculos.all()

    context = {'vehiculos': vehiculos}
    return render(request, 'app1/ver_vehiculos.html', context)


# def index_redirect(request):
#     if 'cliente_id' in request.session:
#         return redirect('home')
#     return redirect('login')
