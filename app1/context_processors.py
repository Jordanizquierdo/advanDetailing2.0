def cart_context(request):
    cart = request.session.get('cart', [])
    total = sum(item['price'] for item in cart)
    return {'cart': cart, 'total': total}
