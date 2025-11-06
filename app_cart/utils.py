"""
Utilidades para el manejo del carrito de compras
"""
from .models import Cart, CartItem
from app_products.models import Product


def migrate_session_cart_to_db(request):
    """
    Migra el carrito de sesión al carrito de base de datos
    Útil cuando un usuario anónimo inicia sesión
    """
    session_cart = request.session.get('cart', {})
    
    if not session_cart or not request.user.is_authenticated:
        return
    
    # Obtener o crear el carrito del usuario
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Migrar items de la sesión al carrito de BD
    for product_id, quantity in session_cart.items():
        try:
            product = Product.objects.get(id=product_id)
            
            # Verificar si el item ya existe
            cart_item, item_created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={'quantity': quantity}
            )
            
            # Si ya existía, actualizar la cantidad
            if not item_created:
                cart_item.quantity += quantity
                # Validar que no exceda el stock
                if cart_item.quantity > product.stock:
                    cart_item.quantity = product.stock
                cart_item.save()
                
        except Product.DoesNotExist:
            continue
    
    # Limpiar el carrito de sesión
    request.session['cart'] = {}
    request.session.modified = True


def get_cart_total(cart):
    """
    Calcula el total del carrito
    """
    return sum(item.get_subtotal() for item in cart.items.all())


def get_cart_count(cart):
    """
    Obtiene el número total de items en el carrito
    """
    return sum(item.quantity for item in cart.items.all())


def validate_cart_stock(cart):
    """
    Valida que todos los items del carrito tengan stock suficiente
    Retorna una tupla (es_valido, items_invalidos)
    """
    invalid_items = []
    
    for item in cart.items.select_related('product').all():
        if item.quantity > item.product.stock:
            invalid_items.append({
                'item': item,
                'requested': item.quantity,
                'available': item.product.stock
            })
    
    return len(invalid_items) == 0, invalid_items


def clean_unavailable_products(cart):
    """
    Elimina productos no disponibles del carrito
    Retorna el número de items eliminados
    """
    removed_count = 0
    
    for item in cart.items.select_related('product').all():
        if not item.product.available or item.product.stock == 0:
            item.delete()
            removed_count += 1
    
    return removed_count
