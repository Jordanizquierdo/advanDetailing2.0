from django.shortcuts import render

def home(request):
    cart = request.session.get('cart', [])
    total = sum(item['price'] for item in cart)
    data = {'cart': cart, 'total': total}
    return render(request, 'app1/index.html', data)
