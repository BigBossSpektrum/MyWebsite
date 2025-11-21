from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count, Sum, Q
from .models import Category, Product, ProductImage


class ProductImageInline(admin.TabularInline):
    """Inline para gestionar imágenes de productos directamente desde el producto"""
    model = ProductImage
    extra = 1
    fields = ('image', 'image_preview', 'alt_text', 'is_main', 'created_at')
    readonly_fields = ('image_preview', 'created_at')
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 100px; max-width: 100px; object-fit: cover;" />',
                obj.image.url
            )
        return "-"
    image_preview.short_description = "Vista Previa"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Configuración del administrador para Categorías con estadísticas"""
    list_display = ('name', 'slug', 'products_count', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('id', 'created_at', 'updated_at', 'products_count')
    list_per_page = 25
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('name', 'slug', 'description')
        }),
        ('Estadísticas', {
            'fields': ('products_count',)
        }),
        ('Metadatos', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """Optimiza las consultas con annotate"""
        queryset = super().get_queryset(request)
        return queryset.annotate(_products_count=Count('products'))
    
    def products_count(self, obj):
        """Muestra el número de productos en la categoría"""
        if hasattr(obj, '_products_count'):
            count = obj._products_count
        else:
            count = obj.products.count()
        
        if count == 0:
            return format_html('<span style="color: #888;">0</span>')
        return format_html(
            '<a href="/admin/app_products/product/?category__id__exact={}">{}</a>',
            obj.id,
            count
        )
    products_count.short_description = 'Productos'
    products_count.admin_order_field = '_products_count'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Configuración del administrador para Productos con funcionalidades avanzadas"""
    list_display = (
        'name',
        'category',
        'price_formatted',
        'stock_colored',
        'available',
        'images_count',
        'created_at'
    )
    list_filter = (
        'available',
        'category',
        'created_at',
        'updated_at'
    )
    search_fields = ('name', 'description', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('id', 'created_at', 'updated_at', 'images_count')
    list_editable = ('available',)
    list_per_page = 25
    date_hierarchy = 'created_at'
    inlines = [ProductImageInline]
    actions = ['mark_as_available', 'mark_as_unavailable', 'duplicate_products']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('name', 'slug', 'category', 'description')
        }),
        ('Precios y Disponibilidad', {
            'fields': ('price', 'stock', 'available')
        }),
        ('Estadísticas', {
            'fields': ('images_count',)
        }),
        ('Metadatos', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """Optimiza las consultas con select_related y annotate"""
        queryset = super().get_queryset(request)
        return queryset.select_related('category').annotate(
            _images_count=Count('images')
        )
    
    def price_formatted(self, obj):
        """Formatea el precio con símbolo de moneda"""
        return format_html('<strong style="color: #2e7d32;">${}</strong>', f"{obj.price:.2f}")
    price_formatted.short_description = 'Precio'
    price_formatted.admin_order_field = 'price'
    
    def stock_colored(self, obj):
        """Muestra el stock con colores según disponibilidad"""
        if obj.stock == 0:
            color = '#dc3545'
        elif obj.stock < 10:
            color = '#ffc107'
        else:
            color = '#28a745'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.stock
        )
    stock_colored.short_description = 'Stock'
    stock_colored.admin_order_field = 'stock'
    
    def images_count(self, obj):
        """Muestra el número de imágenes del producto"""
        if hasattr(obj, '_images_count'):
            count = obj._images_count
        else:
            count = obj.images.count()
        
        if count == 0:
            return format_html('<span style="color: #dc3545;">⚠ Sin imágenes</span>')
        return format_html('<span style="color: #28a745;">✓ {} imagen(es)</span>', count)
    images_count.short_description = 'Imágenes'
    images_count.admin_order_field = '_images_count'
    
    @admin.action(description='Marcar como disponible')
    def mark_as_available(self, request, queryset):
        updated = queryset.update(available=True)
        self.message_user(request, f'{updated} producto(s) marcado(s) como disponible.')
    
    @admin.action(description='Marcar como no disponible')
    def mark_as_unavailable(self, request, queryset):
        updated = queryset.update(available=False)
        self.message_user(request, f'{updated} producto(s) marcado(s) como no disponible.')
    
    @admin.action(description='Duplicar productos seleccionados')
    def duplicate_products(self, request, queryset):
        duplicated_count = 0
        for product in queryset:
            product.pk = None
            product.name = f"{product.name} (Copia)"
            product.slug = f"{product.slug}-copia"
            product.save()
            duplicated_count += 1
        self.message_user(request, f'{duplicated_count} producto(s) duplicado(s).')


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    """Configuración del administrador para Imágenes de Productos"""
    list_display = ('id', 'product', 'image_preview', 'alt_text', 'is_main', 'created_at')
    list_filter = ('is_main', 'created_at', 'product__category')
    search_fields = ('product__name', 'alt_text')
    readonly_fields = ('id', 'created_at', 'image_preview_large')
    list_editable = ('is_main',)
    list_per_page = 25
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Información de la Imagen', {
            'fields': ('product', 'image', 'image_preview_large', 'alt_text', 'is_main')
        }),
        ('Metadatos', {
            'fields': ('id', 'created_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """Optimiza las consultas con select_related"""
        queryset = super().get_queryset(request)
        return queryset.select_related('product', 'product__category')
    
    def image_preview(self, obj):
        """Vista previa pequeña de la imagen"""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 50px; object-fit: cover; border-radius: 4px;" />',
                obj.image.url
            )
        return "-"
    image_preview.short_description = "Imagen"
    
    def image_preview_large(self, obj):
        """Vista previa grande de la imagen"""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 300px; max-width: 500px; object-fit: contain;" />',
                obj.image.url
            )
        return "-"
    image_preview_large.short_description = "Vista Previa"
