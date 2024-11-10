from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Cliente, Encargado, Servicio, Reserva
from django.contrib.auth.models import User

from django.contrib.auth import get_user_model


class CustomLoginView(LoginView):
    template_name = 'app1/login.html'
    redirect_authenticated_user = True  # Redirige si el usuario ya está autenticado

    def get_success_url(self):
        return reverse_lazy('home')  












# # Vista personalizada para login
# class CustomLoginView(LoginView):
#     template_name = 'app1/login.html'
#     redirect_authenticated_user = True

#     def form_valid(self, form):
#         email = form.cleaned_data.get('useremailname')  # Asegúrate que el campo en el formulario coincida
#         password = form.cleaned_data.get('password')
        
#         # Imprimir los valores de email y password para depuración
#         print("Email ingresado:", email)
#         print("Contraseña ingresada:", password)
        
#         # Buscar usuario por correo electrónico
#         try:
#             user = get_user_model().objects.get(email=email)
#             print("Usuario encontrado:", user)
#         except get_user_model().DoesNotExist:
#             print("No se encontró usuario con el correo:", email)
#             messages.error(self.request, "Correo o contraseña incorrectos.")
#             return redirect('login')

#         # Autenticar usuario por correo y contraseña
#         user = authenticate(self.request, email=user.email, password=password)
#         if user is not None:
#             print("Autenticación exitosa para el usuario:", user)
#             login(self.request, user)
#             return redirect(self.get_success_url())
#         else:
#             print("Error de autenticación: correo o contraseña incorrectos.")
#             messages.error(self.request, "Correo o contraseña incorrectos.")
#             return redirect('login')

#     def get_success_url(self):
#         # Redirige según el perfil del usuario
#         if hasattr(self.request.user, 'encargado'):
#             print("Redirigiendo a panel de administración.")
#             return reverse_lazy('index_admin')  # Panel de administración
#         elif hasattr(self.request.user, 'cliente'):
#             print("Redirigiendo a página principal de cliente.")
#             return reverse_lazy('home')  # Página principal de cliente
#         print("Redirigiendo a página principal por defecto.")
#         return reverse_lazy('home')

# Vista de inicio para clientes
@login_required
def home(request):
    cart = request.session.get('cart', [])
    total = sum(item['price'] for item in cart)  # Calcula el total del carrito
    context = {'cart': cart, 'total': total}
    return render(request, 'app1/index_user.html', context)

# Vista para ver el carrito
@login_required
def carrito(request):
    cart = request.session.get('cart', [])
    total = sum(item['price'] for item in cart)  # Calcula el total del carrito
    context = {'cart': cart, 'total': total}
    return render(request, 'app1/carrito.html', context)

# Vista para agregar servicios al carrito
@login_required
def agregar_al_carrito(request, servicio_id):
    servicio = get_object_or_404(Servicio, id=servicio_id)
    item = {'id': servicio.id, 'name': servicio.nombre, 'price': servicio.precio}
    cart = request.session.get('cart', [])
    cart.append(item)  # Agrega el artículo al carrito
    request.session['cart'] = cart  # Guarda el carrito actualizado
    return redirect('home')

# Vista para eliminar servicios del carrito
@login_required
def eliminar_del_carrito(request, servicio_id):
    cart = request.session.get('cart', [])
    cart = [item for item in cart if item['id'] != servicio_id]  # Filtra los elementos a eliminar
    request.session['cart'] = cart  # Guarda el carrito actualizado
    return redirect('carrito')

# Vista de logout
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

# Vista de panel de administración (para encargados)
@login_required
def index_admin(request):
    return render(request, 'app1/index_admin.html')

# Vista de registro
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['password1'] == form.cleaned_data['password2']:
                user = form.save()
                # Crea el perfil de acuerdo al tipo seleccionado
                if form.cleaned_data.get('is_encargado', False):
                    Encargado.objects.create(usuario=user, nombre=user.username)
                else:
                    Cliente.objects.create(usuario=user, nombre=user.username)

                messages.success(request, 'Cuenta creada exitosamente')
                return redirect('login')
            else:
                messages.error(request, 'Las contraseñas no coinciden')
    else:
        form = RegisterForm()
    return render(request, 'app1/register.html', {'form': form})