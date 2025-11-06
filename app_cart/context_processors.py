"""
Context processors para el carrito de compras
"""
from .models import Cart


def cart_context(request):
    """
    Agrega información del carrito al contexto de todas las plantillas
    """
    cart = None
    cart_count = 0
    
    try:
        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user).first()
        else:
            if request.session.session_key:
                cart = Cart.objects.filter(session_key=request.session.session_key).first()
        
        if cart:
            cart_count = cart.get_total_items()
    except:
        pass
    
    return {
        'cart_count': cart_count,
    }
