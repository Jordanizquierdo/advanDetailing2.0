def cart_context(request):
    """
    Contexto de carrito de compras para plantillas.

    Esta función proporciona información del carrito de compras almacenado en la sesión 
    actual del usuario. Calcula el total del carrito y devuelve el contexto 
    necesario para su uso en las plantillas.

    Args:
        request (HttpRequest): Objeto de la solicitud HTTP actual.

    Returns:
        dict: Un diccionario con:
            - 'cart' (list): Lista de elementos en el carrito, cada uno como un diccionario 
              que incluye al menos el precio de cada artículo.
            - 'total' (float): Suma total de los precios de todos los artículos en el carrito.
    
    Ejemplo de uso:
        - Usar en plantillas para mostrar detalles del carrito y el total:
          {{ cart }}   # Muestra el contenido del carrito
          {{ total }}  # Muestra el precio total
    """
    cart = request.session.get('cart', [])
    total = sum(item['price'] for item in cart)
    return {'cart': cart, 'total': total}
