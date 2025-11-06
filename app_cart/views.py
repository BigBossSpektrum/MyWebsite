from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from app_products.models import Product


def cart_view(request):
    """Vista del carrito de compras"""
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0
    
    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=product_id)
            subtotal = product.price * quantity
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal
            })
            total += subtotal
        except Product.DoesNotExist:
            pass
    
    return render(request, 'products/cart.html', {
        'cart_items': cart_items,
        'cart_total': total
    })


def add_to_cart(request, product_id):
    """Añadir producto al carrito"""
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        product = get_object_or_404(Product, id=product_id)
        
        if product.stock < quantity:
            messages.error(request, 'No hay suficiente stock disponible.')
            return redirect('products:product_list')
        
        cart = request.session.get('cart', {})
        product_id_str = str(product_id)
        
        # Si el producto ya está en el carrito, incrementar la cantidad
        if product_id_str in cart:
            cart[product_id_str] += quantity
        else:
            cart[product_id_str] = quantity
            
        request.session['cart'] = cart
        messages.success(request, f'{product.name} agregado al carrito.')
        
    return redirect('cart:cart_view')


def update_cart(request, product_id):
    """Actualizar cantidad de producto en el carrito"""
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 0))
        cart = request.session.get('cart', {})
        product_id_str = str(product_id)
        
        if quantity > 0:
            product = get_object_or_404(Product, id=product_id)
            if product.stock < quantity:
                messages.error(request, 'No hay suficiente stock disponible.')
            else:
                cart[product_id_str] = quantity
                messages.success(request, 'Carrito actualizado.')
        else:
            cart.pop(product_id_str, None)
            messages.success(request, 'Producto eliminado del carrito.')
            
        request.session['cart'] = cart
        
    return redirect('cart:cart_view')


def remove_from_cart(request, product_id):
    """Eliminar producto del carrito"""
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        product_id_str = str(product_id)
        cart.pop(product_id_str, None)
        request.session['cart'] = cart
        messages.success(request, 'Producto eliminado del carrito.')
    return redirect('cart:cart_view')


@login_required
def checkout(request):
    """Proceso de checkout - será implementado con app_orders"""
    messages.info(request, 'La función de checkout estará disponible próximamente.')
    return redirect('cart:cart_view')
