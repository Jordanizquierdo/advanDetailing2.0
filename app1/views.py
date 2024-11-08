from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import FormularioRegistro, FormularioLogin


def home(request):
    cart = request.session.get('cart', [])
    total = sum(item['price'] for item in cart)
    data = {'cart': cart, 'total': total}
    return render(request, 'app1/index.html', data)

def login_view(request):
    if request.method == 'POST':
        form = FormularioLogin(request, data=request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data['username_or_email']
            password = form.cleaned_data['password']
            
            # esto autentica que sea por usuario o por email
            user = authenticate(request, username=username_or_email, password=password)
            if not user:
                try:
                    user_obj = User.objects.get(email=username_or_email)
                    user = authenticate(request, username=user_obj.username, password=password)
                except User.DoesNotExist:
                    pass
            
            if user:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Credenciales incorrectas. Inténtelo de nuevo.')
    else:
        form = FormularioLogin()

    return render(request, 'app1/login.html', {'form': form})



def registrar(request):
    if request.method == 'POST':
        form = FormularioRegistro(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.set_password(form.cleaned_data['password'])
            usuario.save()
            login(request, usuario)
            return redirect('index')
    else:
        form = FormularioRegistro()
    return render(request, 'app1/registro.html', {'form': form})

