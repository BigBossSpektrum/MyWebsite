"""
EJEMPLOS DE USO DEL CRUD DEL CARRITO DESDE PYTHON
Este archivo contiene ejemplos de cómo interactuar con el sistema de carrito desde vistas
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from app_cart.models import Cart, CartItem
from app_cart.views import get_or_create_cart
from app_cart.utils import validate_cart_stock, clean_unavailable_products
from app_products.models import Product


# ========================================
# EJEMPLO 1: OBTENER O CREAR CARRITO
# ========================================
def ejemplo_obtener_carrito(request):
    """
    Obtiene el carrito del usuario actual (autenticado o anónimo)
    """
    cart = get_or_create_cart(request)
    
    # Información del carrito
    total_items = cart.get_total_items()
    total_price = cart.get_total()
    
    context = {
        'cart': cart,
        'total_items': total_items,
        'total_price': total_price
    }
    return render(request, 'mi_template.html', context)


# ========================================
# EJEMPLO 2: AGREGAR PRODUCTO (CREATE)
# ========================================
def ejemplo_agregar_producto(request, product_id):
    """
    Agrega un producto al carrito con validaciones completas
    """
    product = get_object_or_404(Product, id=product_id, available=True)
    cart = get_or_create_cart(request)
    quantity = int(request.POST.get('quantity', 1))
    
    # Validar stock
    if quantity > product.stock:
        messages.error(request, f'Solo hay {product.stock} unidades disponibles.')
        return redirect('products:product_detail', product_id=product_id)
    
    # Intentar obtener o crear el item
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity}
    )
    
    if not created:
        # El item ya existía, actualizar cantidad
        new_quantity = cart_item.quantity + quantity
        if new_quantity > product.stock:
            messages.error(
                request, 
                f'No puedes agregar más. Stock disponible: {product.stock}, '
                f'ya tienes {cart_item.quantity} en el carrito.'
            )
        else:
            cart_item.quantity = new_quantity
            cart_item.save()
            messages.success(request, f'Cantidad actualizada: {cart_item.quantity}')
    else:
        messages.success(request, f'{product.name} agregado al carrito.')
    
    return redirect('cart:cart_view')


# ========================================
# EJEMPLO 3: LEER ITEMS DEL CARRITO (READ)
# ========================================
def ejemplo_leer_carrito(request):
    """
    Lee y muestra todos los items del carrito
    """
    cart = get_or_create_cart(request)
    
    # Obtener todos los items con sus productos (optimizado)
    cart_items = cart.items.select_related('product').all()
    
    # Procesar cada item
    items_data = []
    for item in cart_items:
        items_data.append({
            'product_name': item.product.name,
            'quantity': item.quantity,
            'unit_price': item.product.price,
            'subtotal': item.get_subtotal(),
            'stock_available': item.product.stock,
            'has_enough_stock': item.quantity <= item.product.stock
        })
    
    context = {
        'cart_items': items_data,
        'cart_total': cart.get_total(),
        'total_items': cart.get_total_items()
    }
    return render(request, 'cart_view.html', context)


# ========================================
# EJEMPLO 4: ACTUALIZAR CANTIDAD (UPDATE)
# ========================================
def ejemplo_actualizar_cantidad(request, product_id):
    """
    Actualiza la cantidad de un producto en el carrito
    """
    cart = get_or_create_cart(request)
    product = get_object_or_404(Product, id=product_id)
    new_quantity = int(request.POST.get('quantity', 1))
    
    try:
        cart_item = CartItem.objects.get(cart=cart, product=product)
        
        if new_quantity <= 0:
            # Si la cantidad es 0 o negativa, eliminar el item
            cart_item.delete()
            messages.success(request, f'{product.name} eliminado del carrito.')
        elif new_quantity > product.stock:
            messages.error(request, f'Stock insuficiente. Disponible: {product.stock}')
        else:
            cart_item.quantity = new_quantity
            cart_item.save()
            messages.success(request, 'Cantidad actualizada correctamente.')
            
    except CartItem.DoesNotExist:
        messages.error(request, 'El producto no está en tu carrito.')
    
    return redirect('cart:cart_view')


# ========================================
# EJEMPLO 5: ELIMINAR ITEM (DELETE)
# ========================================
def ejemplo_eliminar_item(request, product_id):
    """
    Elimina un producto específico del carrito
    """
    cart = get_or_create_cart(request)
    product = get_object_or_404(Product, id=product_id)
    
    deleted_count, _ = CartItem.objects.filter(
        cart=cart, 
        product=product
    ).delete()
    
    if deleted_count > 0:
        messages.success(request, f'{product.name} eliminado del carrito.')
    else:
        messages.warning(request, 'El producto no estaba en tu carrito.')
    
    return redirect('cart:cart_view')


# ========================================
# EJEMPLO 6: VACIAR CARRITO (DELETE)
# ========================================
def ejemplo_vaciar_carrito(request):
    """
    Elimina todos los items del carrito
    """
    cart = get_or_create_cart(request)
    
    items_count = cart.get_total_items()
    cart.clear()
    
    messages.success(request, f'Carrito vaciado. {items_count} items eliminados.')
    return redirect('products:product_list')


# ========================================
# EJEMPLO 7: VALIDAR STOCK DEL CARRITO
# ========================================
def ejemplo_validar_stock(request):
    """
    Valida que todos los items tengan stock suficiente
    """
    cart = get_or_create_cart(request)
    
    is_valid, invalid_items = validate_cart_stock(cart)
    
    if not is_valid:
        for item_info in invalid_items:
            item = item_info['item']
            messages.warning(
                request,
                f'{item.product.name}: solicitaste {item_info["requested"]}, '
                f'pero solo hay {item_info["available"]} disponibles.'
            )
            
            # Ajustar automáticamente a stock disponible
            if item_info['available'] > 0:
                item.quantity = item_info['available']
                item.save()
            else:
                item.delete()
        
        messages.info(request, 'Tu carrito ha sido actualizado según el stock disponible.')
    
    return redirect('cart:cart_view')


# ========================================
# EJEMPLO 8: LIMPIAR PRODUCTOS NO DISPONIBLES
# ========================================
def ejemplo_limpiar_no_disponibles(request):
    """
    Elimina productos no disponibles del carrito
    """
    cart = get_or_create_cart(request)
    
    removed_count = clean_unavailable_products(cart)
    
    if removed_count > 0:
        messages.info(
            request, 
            f'{removed_count} producto(s) no disponible(s) eliminado(s) del carrito.'
        )
    
    return redirect('cart:cart_view')


# ========================================
# EJEMPLO 9: AGREGAR MÚLTIPLES PRODUCTOS
# ========================================
def ejemplo_agregar_multiples(request):
    """
    Agrega múltiples productos al carrito de una vez
    """
    cart = get_or_create_cart(request)
    
    # Lista de productos a agregar: [(product_id, quantity), ...]
    products_to_add = [
        ('uuid-producto-1', 2),
        ('uuid-producto-2', 1),
        ('uuid-producto-3', 3),
    ]
    
    added_count = 0
    for product_id, quantity in products_to_add:
        try:
            product = Product.objects.get(id=product_id, available=True)
            
            if quantity <= product.stock:
                cart_item, created = CartItem.objects.get_or_create(
                    cart=cart,
                    product=product,
                    defaults={'quantity': quantity}
                )
                
                if not created:
                    cart_item.quantity += quantity
                    if cart_item.quantity <= product.stock:
                        cart_item.save()
                        added_count += 1
                else:
                    added_count += 1
                    
        except Product.DoesNotExist:
            continue
    
    messages.success(request, f'{added_count} productos agregados al carrito.')
    return redirect('cart:cart_view')


# ========================================
# EJEMPLO 10: OBTENER RESUMEN DEL CARRITO
# ========================================
def ejemplo_resumen_carrito(request):
    """
    Obtiene un resumen completo del carrito
    """
    cart = get_or_create_cart(request)
    
    resumen = {
        'numero_items': cart.get_total_items(),
        'subtotal': cart.get_total(),
        'impuestos': cart.get_total() * 0.16,  # IVA 16%
        'envio': 50.00,  # Costo fijo de envío
    }
    
    resumen['total'] = resumen['subtotal'] + resumen['impuestos'] + resumen['envio']
    
    # Desglose por producto
    resumen['productos'] = []
    for item in cart.items.select_related('product').all():
        resumen['productos'].append({
            'nombre': item.product.name,
            'cantidad': item.quantity,
            'precio_unitario': float(item.product.price),
            'subtotal': float(item.get_subtotal())
        })
    
    return resumen


# ========================================
# EJEMPLO 11: CHECKOUT BÁSICO
# ========================================
@login_required
def ejemplo_checkout(request):
    """
    Proceso de checkout básico
    """
    cart = get_or_create_cart(request)
    
    # Validar que el carrito no esté vacío
    if cart.get_total_items() == 0:
        messages.warning(request, 'Tu carrito está vacío.')
        return redirect('products:product_list')
    
    # Validar stock
    is_valid, invalid_items = validate_cart_stock(cart)
    if not is_valid:
        messages.error(
            request, 
            'Algunos productos no tienen stock suficiente. '
            'Por favor revisa tu carrito.'
        )
        return redirect('cart:cart_view')
    
    # Aquí iría la lógica de crear la orden
    # from app_orders.models import Order, OrderItem
    # order = Order.objects.create(...)
    # for item in cart.items.all():
    #     OrderItem.objects.create(order=order, ...)
    
    messages.success(request, 'Orden creada exitosamente!')
    
    # Vaciar el carrito después del checkout
    cart.clear()
    
    return redirect('orders:order_detail', order_id='...')


# ========================================
# EJEMPLO 12: MIGRAR CARRITO AL LOGIN
# ========================================
def ejemplo_post_login(request):
    """
    Esta función se ejecuta automáticamente gracias al signal
    pero aquí está el ejemplo de cómo funciona
    """
    from app_cart.utils import migrate_session_cart_to_db
    
    # Esto se ejecuta automáticamente al hacer login
    # gracias al signal en signals.py
    migrate_session_cart_to_db(request)
    
    messages.success(request, 'Tu carrito ha sido restaurado.')
    return redirect('home')


# ========================================
# EJEMPLO 13: API VIEW PARA AJAX
# ========================================
from django.http import JsonResponse

def ejemplo_api_cart_info(request):
    """
    API endpoint para obtener información del carrito en JSON
    """
    cart = get_or_create_cart(request)
    
    data = {
        'success': True,
        'cart': {
            'count': cart.get_total_items(),
            'total': float(cart.get_total()),
            'items': []
        }
    }
    
    for item in cart.items.select_related('product').all():
        data['cart']['items'].append({
            'id': str(item.id),
            'product_id': str(item.product.id),
            'product_name': item.product.name,
            'quantity': item.quantity,
            'unit_price': float(item.product.price),
            'subtotal': float(item.get_subtotal()),
            'stock': item.product.stock
        })
    
    return JsonResponse(data)


# ========================================
# EJEMPLO 14: CONTEXT PROCESSOR PERSONALIZADO
# ========================================
def ejemplo_context_processor(request):
    """
    Este es un ejemplo de cómo funciona el context processor
    Ya está implementado en context_processors.py
    """
    cart = None
    cart_info = {
        'cart_count': 0,
        'cart_total': 0,
        'has_items': False
    }
    
    try:
        cart = get_or_create_cart(request)
        cart_info['cart_count'] = cart.get_total_items()
        cart_info['cart_total'] = float(cart.get_total())
        cart_info['has_items'] = cart_info['cart_count'] > 0
    except:
        pass
    
    return cart_info


# ========================================
# EJEMPLO 15: AGREGAR CON TRY-EXCEPT COMPLETO
# ========================================
def ejemplo_agregar_robusto(request, product_id):
    """
    Versión robusta con manejo completo de errores
    """
    try:
        # Obtener producto
        product = Product.objects.get(id=product_id)
        
        # Verificar disponibilidad
        if not product.available:
            messages.error(request, f'{product.name} no está disponible.')
            return redirect('products:product_list')
        
        # Obtener carrito
        cart = get_or_create_cart(request)
        
        # Obtener cantidad
        try:
            quantity = int(request.POST.get('quantity', 1))
            if quantity < 1:
                raise ValueError('La cantidad debe ser al menos 1')
        except ValueError as e:
            messages.error(request, 'Cantidad inválida.')
            return redirect('products:product_detail', product_id=product_id)
        
        # Verificar stock
        if quantity > product.stock:
            messages.error(
                request, 
                f'Stock insuficiente. Disponible: {product.stock}'
            )
            return redirect('products:product_detail', product_id=product_id)
        
        # Agregar o actualizar item
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not created:
            new_quantity = cart_item.quantity + quantity
            if new_quantity > product.stock:
                messages.error(
                    request,
                    f'No puedes agregar {quantity} más. Ya tienes {cart_item.quantity} '
                    f'en el carrito y solo hay {product.stock} disponibles.'
                )
                return redirect('products:product_detail', product_id=product_id)
            
            cart_item.quantity = new_quantity
            cart_item.save()
            messages.success(
                request, 
                f'{product.name} actualizado. Nueva cantidad: {cart_item.quantity}'
            )
        else:
            messages.success(request, f'{product.name} agregado al carrito.')
        
        return redirect('cart:cart_view')
        
    except Product.DoesNotExist:
        messages.error(request, 'El producto no existe.')
        return redirect('products:product_list')
    except Exception as e:
        messages.error(request, f'Error al agregar al carrito: {str(e)}')
        return redirect('products:product_list')
