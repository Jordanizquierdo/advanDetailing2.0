import json
from datetime import datetime
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.utils.timezone import now
from .models import Clientes, Encargado, Reservas, Servicios, Vehiculo,Reviews
from .forms import CustomAuthenticationForm, ClienteForm, VehiculoFormSet
from django.http import JsonResponse
from django.db import connection


def login_view(request):
    form = CustomAuthenticationForm()

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password").strip()

        # Validar si se recibió email y contraseña
        if not email or not password:
            messages.error(request, "Por favor, ingrese todos los campos.")
            return render(request, "app1/login.html", {"form": form})

        # Autenticación del encargado primero
        try:
            encargado = Encargado.objects.get(correo__iexact=email)
            if check_password(password, encargado.password):
                request.session['encargado_id'] = encargado.id
                return redirect("index_admin")
            else:
                messages.error(request, "Contraseña incorrecta para encargado.")
        except Encargado.DoesNotExist:
            # Continúa con cliente si no existe el encargado
            pass

        # Autenticación del cliente
        try:
            cliente = Clientes.objects.get(email__iexact=email)
            if check_password(password, cliente.password):
                request.session['cliente_id'] = cliente.id
                return redirect("/home")
            else:
                messages.error(request, "Contraseña incorrecta para cliente.")
        except Clientes.DoesNotExist:
            # Si no se encuentra en ninguno de los modelos
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
    reservas = Reservas.objects.select_related('cliente', 'vehiculo').all()
    context = {
        'reservas': reservas,
    }
    return render(request, 'app1/index_admin.html', context)

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




def ver_clientes(request):
    clientes = Clientes.objects.prefetch_related('vehiculos').all()
    context = {
        'clientes': clientes,
    }
    return render(request, 'app1/ver_clientes_admin.html', context)


def ver_vehiculos_admin(request):
    vehiculos = Vehiculo.objects.select_related('cliente').all()
    context = {
        'vehiculos': vehiculos,
    }
    return render(request, 'app1/ver_vehiculos_admin.html', context)

def ver_reservas_admin(request):
    reservas_futuras = Reservas.objects.filter(hora_reserva__gte=now()).select_related('cliente', 'vehiculo').prefetch_related('servicios')
    reservas_pasadas = Reservas.objects.filter(hora_reserva__lt=now()).select_related('cliente', 'vehiculo').prefetch_related('servicios')

    if request.method == 'POST':
        reserva_id = request.POST.get('reserva_id')
        nueva_estado = request.POST.get('estado')
        try:
            reserva = Reservas.objects.get(id=reserva_id)
            reserva.estado = nueva_estado
            reserva.save()
        except Reservas.DoesNotExist:
            messages.error(request, "La reserva no existe.")

    context = {
        'reservas_futuras': reservas_futuras,
        'reservas_pasadas': reservas_pasadas,
    }
    return render(request, 'app1/ver_reservas_admin.html', context)


def cliente_vehiculos(request, cliente_id):
    try:
        cliente = Clientes.objects.prefetch_related('vehiculos').get(id=cliente_id)
        vehiculos = cliente.vehiculos.values('modelo', 'year', 'patente')
        return JsonResponse({'vehiculos': list(vehiculos)})
    except Clientes.DoesNotExist:
        return JsonResponse({'error': 'Cliente no encontrado'}, status=404)

def vision_view(request):
    return render(request, 'app1/vision.html')

def quienes_somos_view(request):
    return render(request, 'app1/quienes-somos.html')

def mision_view(request):
    return render(request, 'app1/mision.html')



def agregar_resena_view(request):
    if request.method == 'POST':
        cliente_id = request.session.get('cliente_id')
        vehiculo_id = request.POST.get('vehiculo_id')
        comentarios = request.POST.get('comentarios')
        calificacion = request.POST.get('calificacion')

        errores = []

        # Validaciones de los campos
        if not cliente_id:
            errores.append('No se encontró un cliente asociado. Por favor, inicia sesión.')
        if not vehiculo_id:
            errores.append('El campo "Vehículo" es obligatorio.')
        if not comentarios or comentarios.strip() == "":
            errores.append('El campo "Comentarios" es obligatorio.')
        if not calificacion:
            errores.append('El campo "Calificación" es obligatorio.')
        elif not calificacion.isdigit() or int(calificacion) not in range(1, 6):
            errores.append('La calificación debe ser un número entre 1 y 5.')

        # Mostrar los errores, si existen
        if errores:
            for error in errores:
                messages.error(request, error)
            return redirect('agregar_resena')

        # Proceder a guardar la reseña si no hay errores
        try:
            with connection.cursor() as cursor:
                cursor.callproc('app1_crear_resena', [cliente_id, vehiculo_id, comentarios, calificacion])
            messages.success(request, 'Reseña agregada exitosamente.')
        except Exception as e:
            messages.error(request, f'Hubo un problema al guardar la reseña: {e}')

        return redirect('ver_resenas')

    # Obtener los vehículos del cliente para el formulario
    cliente_id = request.session.get('cliente_id')
    vehiculos = Vehiculo.objects.filter(cliente_id=cliente_id) if cliente_id else []

    return render(request, 'app1/agregar_resena.html', {'vehiculos': vehiculos})


def ver_resenas_view(request):
    cliente_id = request.session.get('cliente_id')

    mis_resenas = []
    todas_resenas = []

    # Obtener reseñas del cliente autenticado
    if cliente_id:
        with connection.cursor() as cursor:
            cursor.callproc('app1_obtener_resenas_por_cliente', [cliente_id])
            for row in cursor.fetchall():
                mis_resenas.append({
                    'id': row[0],
                    'comentarios': row[1],
                    'calificacion': row[2],
                    'fecha_review': row[3],
                    'vehiculo': f"{row[5]} {row[6]} ({row[7]})",  # Marca, modelo y patente
                })

    # Obtener todas las reseñas disponibles
    with connection.cursor() as cursor:
        cursor.callproc('app1_obtener_todas_resenas')
        for row in cursor.fetchall():
            todas_resenas.append({
                'id': row[0],
                'comentarios': row[1],
                'calificacion': row[2],
                'fecha_review': row[3],
                'cliente_nombre': row[4],
                'vehiculo': f"{row[5]} {row[6]} ({row[7]})",  # Marca, modelo y patente
            })

    return render(request, 'app1/ver_resenas.html', {
        'mis_resenas': mis_resenas,
        'todas_resenas': todas_resenas,
    })


def actualizar_resena(request, resena_id):
    # Verificar si el cliente está autenticado
    cliente_id = request.session.get('cliente_id')
    if not cliente_id:
        return redirect('login')

    # Obtener la reseña para mostrar los datos actuales en el formulario
    resena = get_object_or_404(Reviews, id=resena_id, cliente_id=cliente_id)

    if request.method == 'POST':
        comentarios = request.POST.get('comentarios')
        calificacion = request.POST.get('calificacion')

        # Validar que los campos estén completos
        if not comentarios or not calificacion:
            messages.error(request, 'Todos los campos son requeridos.')
            return redirect('actualizar_resena', resena_id=resena_id)

        try:
            # Llamar al procedimiento almacenado para actualizar la reseña
            with connection.cursor() as cursor:
                cursor.callproc('app1_actualizar_resena', [resena_id, comentarios, calificacion])
            messages.success(request, 'Reseña actualizada exitosamente.')
            return redirect('ver_resenas')  # Redirigir a la página de todas las reseñas
        except Exception as e:
            messages.error(request, f'Error al actualizar la reseña: {str(e)}')

    return render(request, 'app1/actualizar_resena.html', {'resena': resena})




def eliminar_resena(request, resena_id):
    if request.method == 'POST':
        try:
            # Llamar al procedimiento almacenado para eliminar la reseña
            with connection.cursor() as cursor:
                cursor.callproc('app1_eliminar_resena', [resena_id])
            messages.success(request, 'Reseña eliminada exitosamente.')
        except Exception as e:
            messages.error(request, f'Error al eliminar la reseña: {str(e)}')

    return redirect('ver_resenas')