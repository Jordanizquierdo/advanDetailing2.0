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
    """
    Maneja el proceso de inicio de sesión para los modelos 'Encargado' y 'Clientes'.
    
    Args:
        request: El objeto de solicitud HTTP que contiene metadatos sobre la solicitud.
    
    Returns:
        HttpResponse: Redirige a la página correspondiente si el inicio de sesión es exitoso o 
                      vuelve a renderizar la página de inicio de sesión con mensajes de error si no es así.
    
    Flujo de trabajo:
        1. Renderiza un formulario CustomAuthenticationForm vacío.
        2. Si se hace una solicitud POST, valida el correo electrónico y la contraseña proporcionados:
           - Primero, verifica si el correo electrónico pertenece a un 'Encargado'.
           - Si no, verifica si el correo electrónico pertenece a un 'Cliente'.
        3. Si la autenticación es exitosa:
           - Redirige a los usuarios 'Encargado' a 'index_admin'.
           - Redirige a los usuarios 'Cliente' a '/home'.
        4. Si la autenticación falla, muestra los mensajes de error correspondientes.
    
    Notas:
        - 'Encargado' y 'Clientes' son dos modelos de usuario separados.
        - La validación de contraseñas se realiza utilizando `check_password`.
    """
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
            # Si no se encuentra, continúa con cliente
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
    """
    Maneja el cierre de sesión del usuario, eliminando la sesión activa.
    
    Args:
        request: El objeto de solicitud HTTP que contiene metadatos sobre la solicitud.
    
    Returns:
        HttpResponse: Redirige al usuario a la página de inicio ('home').
    """
    request.session.flush()
    return redirect('home')


def home(request):
    """
    Muestra la página de inicio del cliente, con información sobre el carrito y el cliente si está autenticado.
    
    Args:
        request: El objeto de solicitud HTTP que contiene metadatos sobre la solicitud.
    
    Returns:
        HttpResponse: Renderiza la página 'index_user.html' con los datos del carrito de compras y del cliente.
    
    Notas:
        - Si el cliente está autenticado, muestra los detalles de su cuenta.
        - Calcula el total del carrito sumando los precios de los productos.
    """
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
    """
    Muestra la página de administración con la lista de reservas de los clientes.
    
    Args:
        request: El objeto de solicitud HTTP que contiene metadatos sobre la solicitud.
    
    Returns:
        HttpResponse: Renderiza la página 'index_admin.html' con la lista de reservas.
    
    Notas:
        - Se obtienen todas las reservas relacionadas con clientes y vehículos utilizando select_related para optimizar las consultas.
    """
    reservas = Reservas.objects.select_related('cliente', 'vehiculo').all()
    context = {
        'reservas': reservas,
    }
    return render(request, 'app1/index_admin.html', context)

def carrito(request):
    """
    Muestra la página del carrito de compras, con la posibilidad de proceder a la reserva de un servicio.
    
    Args:
        request: El objeto de solicitud HTTP que contiene metadatos sobre la solicitud.
    
    Returns:
        HttpResponse: Renderiza la página 'carrito.html' con los elementos del carrito y el total.
    
    Flujo de trabajo:
        1. Verifica si el cliente está autenticado.
        2. Si no está autenticado, redirige al inicio de sesión.
        3. Si el cliente está autenticado, obtiene los vehículos asociados al cliente.
        4. Si se envía una solicitud POST, se intenta crear una reserva con la fecha, hora y vehículo seleccionados.
        5. Si la reserva se crea correctamente, se asocian los servicios del carrito y se redirige a la página de inicio.
    """
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
    """
    Registra un nuevo cliente y sus vehículos asociados.
    
    Args:
        request: El objeto de solicitud HTTP que contiene metadatos sobre la solicitud.
    
    Returns:
        HttpResponse: Redirige a la página de inicio ('/') si el registro es exitoso.
    
    Flujo de trabajo:
        1. Si se hace una solicitud POST, se validan los formularios de cliente y vehículos.
        2. Si los formularios son válidos, se guarda el cliente y sus vehículos en la base de datos.
        3. Si no se hace una solicitud POST, se muestra el formulario vacío.
    """
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
    """
    Muestra las reservas futuras y pasadas de un cliente autenticado.

    Args:
        request: El objeto de solicitud HTTP que contiene metadatos sobre la solicitud.

    Returns:
        HttpResponse: Renderiza la página 'reservas.html' con las reservas futuras y pasadas.

    Notas:
        - Si el cliente no está autenticado, redirige al inicio de sesión.
        - Filtra las reservas futuras y pasadas en función de la hora de reserva.
    """
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
    """
    Permite a un cliente agregar un nuevo vehículo a su cuenta.

    Args:
        request: El objeto de solicitud HTTP que contiene metadatos sobre la solicitud.

    Returns:
        HttpResponse: Redirige a la página 'ver_vehiculos' si el vehículo se agrega correctamente.

    Notas:
        - Si el cliente no está autenticado, redirige al inicio de sesión.
        - Si se hace una solicitud POST, crea un nuevo vehículo asociado al cliente.
    """
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
    """
    Muestra los vehículos asociados a un cliente autenticado.

    Args:
        request: El objeto de solicitud HTTP que contiene metadatos sobre la solicitud.

    Returns:
        HttpResponse: Renderiza la página 'ver_vehiculos.html' con los vehículos del cliente.

    Notas:
        - Si el cliente no está autenticado, redirige al inicio de sesión.
    """
    cliente_id = request.session.get('cliente_id')
    if not cliente_id:
        return redirect('login')

    cliente = Clientes.objects.get(id=cliente_id)
    vehiculos = cliente.vehiculos.all()

    context = {'vehiculos': vehiculos}
    return render(request, 'app1/ver_vehiculos.html', context)


def ver_clientes(request):
    """
    Muestra la lista de clientes en la vista de administración.

    Args:
        request: El objeto de solicitud HTTP que contiene metadatos sobre la solicitud.

    Returns:
        HttpResponse: Renderiza la página 'ver_clientes_admin.html' con todos los clientes.

    Notas:
        - Los vehículos de cada cliente son cargados usando `prefetch_related` para optimizar las consultas.
    """
    clientes = Clientes.objects.prefetch_related('vehiculos').all()
    context = {
        'clientes': clientes,
    }
    return render(request, 'app1/ver_clientes_admin.html', context)


def ver_vehiculos_admin(request):
    """
    Muestra la lista de vehículos en la vista de administración.

    Args:
        request: El objeto de solicitud HTTP que contiene metadatos sobre la solicitud.

    Returns:
        HttpResponse: Renderiza la página 'ver_vehiculos_admin.html' con todos los vehículos.

    Notas:
        - Se cargan los clientes relacionados con cada vehículo utilizando `select_related` para optimizar las consultas.
    """
    vehiculos = Vehiculo.objects.select_related('cliente').all()
    context = {
        'vehiculos': vehiculos,
    }
    return render(request, 'app1/ver_vehiculos_admin.html', context)

def ver_reservas_admin(request):
    """
    Muestra las reservas futuras y pasadas en la vista de administración, y permite actualizar el estado de una reserva.

    Args:
        request: El objeto de solicitud HTTP que contiene metadatos sobre la solicitud.

    Returns:
        HttpResponse: Renderiza la página 'ver_reservas_admin.html' con las reservas filtradas.

    Notas:
        - Se permite cambiar el estado de una reserva usando un formulario POST.
        - Las reservas futuras y pasadas se filtran utilizando la hora de la reserva.
    """
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
    """
    Devuelve los vehículos de un cliente en formato JSON.

    Args:
        request: El objeto de solicitud HTTP que contiene metadatos sobre la solicitud.
        cliente_id: El ID del cliente cuya información de vehículos se desea obtener.

    Returns:
        JsonResponse: Devuelve los vehículos del cliente en formato JSON o un error si el cliente no se encuentra.

    Notas:
        - Si el cliente no existe, devuelve un error 404.
    """
    try:
        cliente = Clientes.objects.prefetch_related('vehiculos').get(id=cliente_id)
        vehiculos = cliente.vehiculos.values('modelo', 'year', 'patente')
        return JsonResponse({'vehiculos': list(vehiculos)})
    except Clientes.DoesNotExist:
        return JsonResponse({'error': 'Cliente no encontrado'}, status=404)


def vision_view(request):
    """
    Muestra la página de la visión de la empresa.

    Args:
        request: El objeto de solicitud HTTP que contiene metadatos sobre la solicitud.

    Returns:
        HttpResponse: Renderiza la página 'vision.html'.
    """
    return render(request, 'app1/vision.html')


def quienes_somos_view(request):
    """
    Muestra la página 'Quienes Somos' de la empresa.

    Args:
        request: El objeto de solicitud HTTP que contiene metadatos sobre la solicitud.

    Returns:
        HttpResponse: Renderiza la página 'quienes-somos.html'.
    """
    return render(request, 'app1/quienes-somos.html')


def mision_view(request):
    """
    Muestra la página de la misión de la empresa.

    Args:
        request: El objeto de solicitud HTTP que contiene metadatos sobre la solicitud.

    Returns:
        HttpResponse: Renderiza la página 'mision.html'.
    """
    return render(request, 'app1/mision.html')














def agregar_resena_view(request):
    """
    Permite a un cliente agregar una reseña sobre un vehículo.

    Args:
        request: El objeto de solicitud HTTP que contiene metadatos sobre la solicitud.

    Returns:
        HttpResponse: Redirige a la página de reseñas si la reseña se agrega correctamente o muestra errores.

    Notas:
        - Si el cliente no está autenticado, redirige al inicio de sesión.
        - Realiza varias validaciones sobre los campos de la reseña.
        - Utiliza un procedimiento almacenado para agregar la reseña en la base de datos.
    """
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
    """
    Muestra las reseñas del cliente autenticado y todas las reseñas disponibles.

    Args:
        request: El objeto de solicitud HTTP que contiene metadatos sobre la solicitud.

    Returns:
        HttpResponse: Renderiza la página 'ver_resenas.html' con las reseñas del cliente y todas las reseñas.

    Notas:
        - Si el cliente está autenticado, se obtienen sus reseñas.
        - Se obtienen todas las reseñas desde la base de datos.
    """
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
    """
    Permite a un cliente actualizar una reseña existente.

    Args:
        request: El objeto de solicitud HTTP que contiene metadatos sobre la solicitud.
        resena_id: El ID de la reseña que se desea actualizar.

    Returns:
        HttpResponse: Redirige a la página de todas las reseñas si se actualiza correctamente.

    Notas:
        - Solo se permite la actualización de reseñas creadas por el cliente autenticado.
        - Realiza una validación de los campos antes de actualizar.
        - Utiliza un procedimiento almacenado para actualizar la reseña en la base de datos.
    """
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
    """
    Permite a un cliente eliminar una reseña existente.

    Args:
        request: El objeto de solicitud HTTP que contiene metadatos sobre la solicitud.
        resena_id: El ID de la reseña que se desea eliminar.

    Returns:
        HttpResponse: Redirige a la página de todas las reseñas si se elimina correctamente.

    Notas:
        - Utiliza un procedimiento almacenado para eliminar la reseña de la base de datos.
    """
    if request.method == 'POST':
        try:
            # Llamar al procedimiento almacenado para eliminar la reseña
            with connection.cursor() as cursor:
                cursor.callproc('app1_eliminar_resena', [resena_id])
            messages.success(request, 'Reseña eliminada exitosamente.')
        except Exception as e:
            messages.error(request, f'Error al eliminar la reseña: {str(e)}')

    return redirect('ver_resenas')






