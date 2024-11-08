from django.shortcuts import render
import json



def home(request):
    cart = request.session.get('cart', [])
    total = sum(item['price'] for item in cart)
    data = {'cart': cart, 'total': total}
    return render(request, 'app1/index.html', data)


def carrito(request):
    cart_data = request.GET.get("cartList", "[]")
    
    try:
        cart_data = json.loads(cart_data)
    except json.JSONDecodeError:
        cart_data = []

    total = sum(item['price'] for item in cart_data)

    context = {
        'cart_items': cart_data,
        'total': total,
    }

    return render(request, 'app1/carrito.html', context)