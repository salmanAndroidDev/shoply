from cart.cart import Cart


def cart(request):
    """Context processor to cart to the request context"""
    return {'cart': Cart(request)}
