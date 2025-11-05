from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Category, Product, ProductImage
from django.http import JsonResponse
from django.db.models import Q

# Vistas para clientes
def product_list(request):
    category_slug = request.GET.get('category')
    categories = Category.objects.all()
    products = Product.objects.filter(stock__gt=0)  # Mostrar productos con stock > 0
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
        
    # Paginación
    page = request.GET.get('page', 1)
    paginator = Paginator(products, 12)  # 12 productos por página
    products = paginator.get_page(page)
    
    context = {
        'categories': categories,
        'products': products,
        'selected_category': category_slug
    }
    return render(request, 'products/product_list.html', context)

def cart_view(request):
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
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        product = get_object_or_404(Product, id=product_id)
        
        if product.stock < quantity:
            messages.error(request, 'No hay suficiente stock disponible.')
            return redirect('products:product_list')
        
        cart = request.session.get('cart', {})
        cart[str(product_id)] = quantity
        request.session['cart'] = cart
        messages.success(request, 'Producto agregado al carrito.')
        
    return redirect('products:cart')

def update_cart(request, product_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 0))
        cart = request.session.get('cart', {})
        
        if quantity > 0:
            product = get_object_or_404(Product, id=product_id)
            if product.stock < quantity:
                messages.error(request, 'No hay suficiente stock disponible.')
            else:
                cart[str(product_id)] = quantity
        else:
            cart.pop(str(product_id), None)
            
        request.session['cart'] = cart
        
    return redirect('products:cart')

def remove_from_cart(request, product_id):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        cart.pop(str(product_id), None)
        request.session['cart'] = cart
        messages.success(request, 'Producto eliminado del carrito.')
    return redirect('products:cart')

@login_required
def checkout(request):
    # Esta función se implementará cuando creemos el sistema de pedidos
    messages.info(request, 'La función de checkout estará disponible próximamente.')
    return redirect('products:cart')

# Vistas para administradores
@staff_member_required
def admin_product_list(request):
    search_query = request.GET.get('search', '')
    category_id = request.GET.get('category')
    products = Product.objects.all()
    
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    if category_id:
        products = products.filter(category_id=category_id)
    
    # Paginación
    page = request.GET.get('page', 1)
    paginator = Paginator(products, 10)  # 10 productos por página
    products = paginator.get_page(page)
    
    categories = Category.objects.all()
    
    return render(request, 'products/admin/product_list.html', {
        'products': products,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_id
    })

@staff_member_required
def admin_product_create(request):
    if request.method == 'POST':
        # Implementar la lógica de creación
        pass
    return render(request, 'products/admin/product_form.html')

@staff_member_required
def admin_product_edit(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        # Implementar la lógica de edición
        pass
    return render(request, 'products/admin/product_form.html', {'product': product})

@staff_member_required
def admin_product_delete(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Producto eliminado exitosamente.')
        return redirect('products:admin_product_list')
    return redirect('products:admin_product_list')

@staff_member_required
def admin_product_images(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'products/admin/product_images.html', {'product': product})

@staff_member_required
def admin_product_images_upload(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST' and request.FILES:
        for image in request.FILES.getlist('images'):
            ProductImage.objects.create(product=product, image=image)
        messages.success(request, 'Imágenes subidas exitosamente.')
    return redirect('products:admin_product_images', product_id=product_id)

@staff_member_required
def admin_product_image_update(request, product_id, image_id):
    image = get_object_or_404(ProductImage, id=image_id, product_id=product_id)
    if request.method == 'POST':
        image.alt_text = request.POST.get('alt_text', '')
        is_main = request.POST.get('is_main') == 'on'
        if is_main:
            # Desmarcar otras imágenes principales
            product = image.product
            product.images.exclude(id=image_id).update(is_main=False)
        image.is_main = is_main
        image.save()
        messages.success(request, 'Imagen actualizada exitosamente.')
    return redirect('products:admin_product_images', product_id=product_id)

@staff_member_required
def admin_product_image_delete(request, product_id, image_id):
    image = get_object_or_404(ProductImage, id=image_id, product_id=product_id)
    if request.method == 'POST':
        image.delete()
        messages.success(request, 'Imagen eliminada exitosamente.')
    return redirect('products:admin_product_images', product_id=product_id)
