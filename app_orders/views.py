from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Order, OrderItem
from app_products.models import Product
from django.db.models import Q
from django.utils import timezone

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    # Paginación
    page = request.GET.get('page', 1)
    paginator = Paginator(orders, 10)
    orders = paginator.get_page(page)
    
    return render(request, 'orders/order_list.html', {'orders': orders})

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    # Paginación
    page = request.GET.get('page', 1)
    paginator = Paginator(orders, 10)
    orders = paginator.get_page(page)
    
    return render(request, 'orders/order_history.html', {'orders': orders})

@login_required
def create_order(request):
    cart = request.session.get('cart', {})
    
    if not cart:
        messages.error(request, 'Tu carrito está vacío.')
        return redirect('cart:cart_view')
    
    # Verificar stock antes de crear la orden
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        if product.stock < quantity:
            messages.error(request, f'No hay suficiente stock de {product.name}.')
            return redirect('cart:cart_view')
    
    # Crear la orden
    order = Order.objects.create(user=request.user, status='pending')
    
    # Crear los items de la orden y actualizar el stock
    total = 0
    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        price = product.price
        subtotal = price * quantity
        
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            price=price,
            subtotal=subtotal
        )
        
        # Actualizar stock
        product.stock -= quantity
        product.save()
        
        total += subtotal
    
    # Actualizar el total de la orden
    order.total = total
    order.save()
    
    # Limpiar el carrito
    request.session['cart'] = {}
    
    messages.success(request, 'Orden creada exitosamente.')
    return redirect('orders:order_detail', order_id=order.id)

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})

@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if order.status == 'pending':
        # Devolver stock
        for item in order.items.all():
            product = item.product
            product.stock += item.quantity
            product.save()
        
        order.status = 'cancelled'
        order.cancelled_at = timezone.now()
        order.save()
        
        messages.success(request, 'Orden cancelada exitosamente.')
    else:
        messages.error(request, 'No se puede cancelar esta orden.')
    
    return redirect('orders:order_detail', order_id=order.id)

# Vistas para administradores
@staff_member_required
def admin_order_list(request):
    status = request.GET.get('status')
    search = request.GET.get('search')
    
    orders = Order.objects.all().order_by('-created_at')
    
    if status:
        orders = orders.filter(status=status)
    
    if search:
        orders = orders.filter(
            Q(id__icontains=search) |
            Q(user__email__icontains=search) |
            Q(user__first_name__icontains=search) |
            Q(user__last_name__icontains=search)
        )
    
    # Paginación
    page = request.GET.get('page', 1)
    paginator = Paginator(orders, 20)
    orders = paginator.get_page(page)
    
    return render(request, 'orders/admin/order_list.html', {
        'orders': orders,
        'selected_status': status,
        'search_query': search
    })

@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/admin/order_detail.html', {'order': order})

@staff_member_required
def admin_order_update(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status and new_status != order.status:
            # Si se cancela una orden, devolver stock
            if new_status == 'cancelled' and order.status != 'cancelled':
                for item in order.items.all():
                    product = item.product
                    product.stock += item.quantity
                    product.save()
            
            order.status = new_status
            if new_status == 'cancelled':
                order.cancelled_at = timezone.now()
            elif new_status == 'completed':
                order.completed_at = timezone.now()
            order.save()
            
            messages.success(request, 'Estado de la orden actualizado.')
        
    return redirect('orders:admin_order_detail', order_id=order.id)


@staff_member_required
def admin_update_order_prices(request, order_id):
    """
    Actualizar los precios de los items de una orden (cotización)
    Los cambios se guardan en los OrderItems sin afectar los precios originales de los productos
    """
    from decimal import Decimal, InvalidOperation
    
    order = get_object_or_404(Order, id=order_id)
    
    if request.method != 'POST':
        messages.error(request, 'Método no permitido')
        return redirect('orders:admin_order_detail', order_id=order.id)
    
    try:
        # Obtener los datos del formulario
        updated_items = []
        errors = []
        
        for item in order.items.all():
            # Obtener el nuevo precio del POST
            new_price_key = f'price_{item.id}'
            new_quantity_key = f'quantity_{item.id}'
            
            if new_price_key in request.POST:
                try:
                    new_price = Decimal(request.POST.get(new_price_key, item.price))
                    new_quantity = int(request.POST.get(new_quantity_key, item.quantity))
                    
                    if new_price < 0:
                        errors.append(f'El precio de {item.product.name if item.product else "item"} no puede ser negativo')
                        continue
                    
                    if new_quantity < 1:
                        errors.append(f'La cantidad de {item.product.name if item.product else "item"} debe ser al menos 1')
                        continue
                    
                    # Actualizar el item
                    old_price = item.price
                    old_quantity = item.quantity
                    
                    item.price = new_price
                    item.quantity = new_quantity
                    item.subtotal = new_price * new_quantity
                    item.save()
                    
                    updated_items.append({
                        'id': str(item.id),
                        'product': item.product.name if item.product else 'N/A',
                        'old_price': float(old_price),
                        'new_price': float(new_price),
                        'old_quantity': old_quantity,
                        'new_quantity': new_quantity,
                        'subtotal': float(item.subtotal)
                    })
                    
                except (ValueError, InvalidOperation) as e:
                    errors.append(f'Error en {item.product.name if item.product else "item"}: valor inválido')
        
        # Recalcular el total de la orden
        new_total = sum(item.subtotal for item in order.items.all())
        order.total = new_total
        order.save()
        
        if errors:
            messages.warning(request, f'Algunos items no se pudieron actualizar: {", ".join(errors)}')
        
        if updated_items:
            messages.success(request, f'Cotización actualizada exitosamente. Nuevo total: ${order.total}')
        else:
            messages.info(request, 'No se realizaron cambios en los precios.')
        
        return redirect('orders:admin_order_detail', order_id=order.id)
        
    except Exception as e:
        messages.error(request, f'Error al actualizar la cotización: {str(e)}')
        return redirect('orders:admin_order_detail', order_id=order.id)
