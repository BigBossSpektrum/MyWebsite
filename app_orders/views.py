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
