from .cart import CartManager

def cart(request):
    if request.user.is_authenticated:
        cart_manager = CartManager(request)
        return {
            'cart_items': cart_manager.get_items(),
            'cart_total': cart_manager.get_total_price(),
            'cart_count': cart_manager.get_total_quantity(),
        }
    return {
        'cart_items': [],
        'cart_total': 0,
        'cart_count': 0,
    }