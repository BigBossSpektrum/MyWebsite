from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Category, Product, ProductImage
from .forms import ProductForm
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

def product_detail(request, slug):
    """Vista detallada de un producto con galería de imágenes"""
    product = get_object_or_404(Product, slug=slug)
    images = product.images.all()
    main_image = product.get_main_image()
    
    # Productos relacionados de la misma categoría
    related_products = Product.objects.filter(
        category=product.category,
        available=True,
        stock__gt=0
    ).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'images': images,
        'main_image': main_image,
        'related_products': related_products,
    }
    return render(request, 'products/product_detail.html', context)

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
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            
            # Procesar imágenes si se subieron
            images = request.FILES.getlist('product_images')
            if images:
                for idx, image in enumerate(images):
                    # La primera imagen será la principal
                    is_main = (idx == 0)
                    ProductImage.objects.create(
                        product=product,
                        image=image,
                        is_main=is_main
                    )
                messages.success(request, f'Producto "{product.name}" creado exitosamente con {len(images)} imagen(es).')
            else:
                messages.success(request, f'Producto "{product.name}" creado exitosamente.')
            
            return redirect('products:admin_product_list')
    else:
        form = ProductForm()
    return render(request, 'products/admin/product_form.html', {'form': form})

@staff_member_required
def admin_product_edit(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            product = form.save()
            
            # Procesar imágenes nuevas si se subieron
            images = request.FILES.getlist('product_images')
            if images:
                for image in images:
                    # Si no hay imágenes principales, hacer la primera como principal
                    is_main = not product.images.filter(is_main=True).exists()
                    ProductImage.objects.create(
                        product=product,
                        image=image,
                        is_main=is_main
                    )
                messages.success(request, f'Producto "{product.name}" actualizado exitosamente con {len(images)} nueva(s) imagen(es).')
            else:
                messages.success(request, f'Producto "{product.name}" actualizado exitosamente.')
            
            return redirect('products:admin_product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/admin/product_form.html', {
        'form': form, 
        'product': product
    })

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
