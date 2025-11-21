from django import template

register = template.Library()


@register.filter(name='sum_quantities')
def sum_quantities(cart_items):
    """
    Suma todas las cantidades de los items en el carrito.
    
    Args:
        cart_items: Lista de items del carrito
        
    Returns:
        int: Suma total de todas las cantidades
    """
    total = 0
    for item in cart_items:
        total += item.quantity
    return total
