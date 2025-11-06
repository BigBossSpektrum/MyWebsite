from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import F
from django.http import JsonResponse
from app_products.models import Product
from .models import Cart, CartItem


def get_or_create_cart(request):
    """
    Obtiene o crea un carrito para el usuario actual o la sesión anónima
    """
    if request.user.is_authenticated:
        # Para usuarios autenticados
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        # Para usuarios anónimos (basado en sesión)
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)
    
    return cart


def cart_view(request):
    """
    READ - Vista del carrito de compras
    Muestra todos los items del carrito
    """
    cart = get_or_create_cart(request)
    cart_items = cart.items.select_related('product').all()
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'cart_total': cart.get_total(),
        'total_items': cart.get_total_items(),
    }
    
    return render(request, 'products/cart.html', context)


def add_to_cart(request, product_id):
    """
    CREATE - Añadir producto al carrito
    Crea un nuevo CartItem o actualiza la cantidad si ya existe
    """
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        product = get_object_or_404(Product, id=product_id)
        
        # Verificar disponibilidad del producto
        if not product.available:
            messages.error(request, f'{product.name} no está disponible actualmente.')
            return redirect('products:product_list')
        
        cart = get_or_create_cart(request)
        
        try:
            # Intentar obtener el item existente
            cart_item = CartItem.objects.get(cart=cart, product=product)
            new_quantity = cart_item.quantity + quantity
            
            # Validar stock
            if new_quantity > product.stock:
                messages.error(
                    request,
                    f'No hay suficiente stock. Stock disponible: {product.stock}, '
                    f'ya tienes {cart_item.quantity} en el carrito.'
                )
                return redirect('products:product_list')
            
            cart_item.quantity = new_quantity
            cart_item.save()
            messages.success(request, f'Cantidad de {product.name} actualizada en el carrito.')
            
        except CartItem.DoesNotExist:
            # Crear nuevo item en el carrito
            if quantity > product.stock:
                messages.error(
                    request,
                    f'No hay suficiente stock disponible. Stock: {product.stock}'
                )
                return redirect('products:product_list')
            
            CartItem.objects.create(
                cart=cart,
                product=product,
                quantity=quantity
            )
            messages.success(request, f'{product.name} agregado al carrito.')
        
    return redirect('cart:cart_view')


def update_cart(request, product_id):
    """
    UPDATE - Actualizar cantidad de producto en el carrito
    Modifica la cantidad de un CartItem existente
    """
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 0))
        product = get_object_or_404(Product, id=product_id)
        cart = get_or_create_cart(request)
        
        try:
            cart_item = CartItem.objects.get(cart=cart, product=product)
            
            if quantity > 0:
                # Validar stock
                if quantity > product.stock:
                    messages.error(
                        request,
                        f'No hay suficiente stock disponible. Stock: {product.stock}'
                    )
                else:
                    cart_item.quantity = quantity
                    cart_item.save()
                    messages.success(request, 'Cantidad actualizada correctamente.')
            else:
                # Si la cantidad es 0, eliminar el item
                cart_item.delete()
                messages.success(request, f'{product.name} eliminado del carrito.')
                
        except CartItem.DoesNotExist:
            messages.error(request, 'El producto no está en tu carrito.')
        except ValueError as e:
            messages.error(request, str(e))
            
    return redirect('cart:cart_view')


def remove_from_cart(request, product_id):
    """
    DELETE - Eliminar producto del carrito
    Elimina un CartItem del carrito
    """
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        cart = get_or_create_cart(request)
        
        try:
            cart_item = CartItem.objects.get(cart=cart, product=product)
            product_name = cart_item.product.name
            cart_item.delete()
            messages.success(request, f'{product_name} eliminado del carrito.')
        except CartItem.DoesNotExist:
            messages.error(request, 'El producto no está en tu carrito.')
            
    return redirect('cart:cart_view')


def clear_cart(request):
    """
    DELETE - Limpiar todo el carrito
    Elimina todos los CartItems del carrito
    """
    if request.method == 'POST':
        cart = get_or_create_cart(request)
        cart.clear()
        messages.success(request, 'Carrito vaciado correctamente.')
    
    return redirect('cart:cart_view')


@login_required
def checkout(request):
    """Proceso de checkout - será implementado con app_orders"""
    cart = get_or_create_cart(request)
    
    if cart.get_total_items() == 0:
        messages.warning(request, 'Tu carrito está vacío.')
        return redirect('cart:cart_view')
    
    messages.info(request, 'La función de checkout estará disponible próximamente.')
    return redirect('cart:cart_view')


# API views para operaciones AJAX (opcional)
def cart_item_count(request):
    """
    API endpoint para obtener el número de items en el carrito
    """
    cart = get_or_create_cart(request)
    return JsonResponse({
        'count': cart.get_total_items(),
        'total': float(cart.get_total())
    })
