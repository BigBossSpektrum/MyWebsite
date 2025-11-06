from django.contrib import admin
from .models import Category, Product, ProductImage


class ProductImageInline(admin.TabularInline):
    """Inline para gestionar imágenes de productos directamente desde el producto"""
    model = ProductImage
    extra = 1
    fields = ('image', 'alt_text', 'is_main')
    readonly_fields = ('created_at',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Configuración del administrador para Categorías"""
    list_display = ('name', 'slug', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('id', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('name', 'slug', 'description')
        }),
        ('Metadatos', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Configuración del administrador para Productos"""
    list_display = ('name', 'category', 'price', 'stock', 'available', 'created_at')
    list_filter = ('available', 'category', 'created_at', 'updated_at')
    search_fields = ('name', 'description', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('id', 'created_at', 'updated_at')
    list_editable = ('price', 'stock', 'available')
    list_per_page = 20
    date_hierarchy = 'created_at'
    inlines = [ProductImageInline]
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('name', 'slug', 'category', 'description')
        }),
        ('Precios y Disponibilidad', {
            'fields': ('price', 'stock', 'available')
        }),
        ('Metadatos', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """Optimiza las consultas con select_related"""
        queryset = super().get_queryset(request)
        return queryset.select_related('category')


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    """Configuración del administrador para Imágenes de Productos"""
    list_display = ('product', 'alt_text', 'is_main', 'created_at')
    list_filter = ('is_main', 'created_at')
    search_fields = ('product__name', 'alt_text')
    readonly_fields = ('id', 'created_at')
    list_editable = ('is_main',)
    
    fieldsets = (
        ('Información de la Imagen', {
            'fields': ('product', 'image', 'alt_text', 'is_main')
        }),
        ('Metadatos', {
            'fields': ('id', 'created_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """Optimiza las consultas con select_related"""
        queryset = super().get_queryset(request)
        return queryset.select_related('product')
