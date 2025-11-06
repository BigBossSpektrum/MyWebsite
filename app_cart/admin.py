from django.contrib import admin
from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    """Inline para mostrar los items del carrito"""
    model = CartItem
    extra = 0
    readonly_fields = ('created_at', 'updated_at', 'get_subtotal_display')
    fields = ('product', 'quantity', 'get_subtotal_display', 'created_at')
    
    def get_subtotal_display(self, obj):
        if obj.id:
            return f"${obj.get_subtotal():.2f}"
        return "-"
    get_subtotal_display.short_description = "Subtotal"


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """Administración de carritos"""
    list_display = (
        'id',
        'get_owner',
        'get_total_items_display',
        'get_total_display',
        'updated_at',
        'created_at'
    )
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user__username', 'user__email', 'session_key')
    readonly_fields = ('id', 'created_at', 'updated_at', 'get_total_display', 'get_total_items_display')
    inlines = [CartItemInline]
    
    fieldsets = (
        ('Información del Carrito', {
            'fields': ('id', 'user', 'session_key')
        }),
        ('Estadísticas', {
            'fields': ('get_total_items_display', 'get_total_display')
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_owner(self, obj):
        if obj.user:
            return obj.user.username
        return f"Anónimo ({obj.session_key[:8]}...)"
    get_owner.short_description = "Propietario"
    
    def get_total_items_display(self, obj):
        return obj.get_total_items()
    get_total_items_display.short_description = "Items Totales"
    
    def get_total_display(self, obj):
        return f"${obj.get_total():.2f}"
    get_total_display.short_description = "Total"


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    """Administración de items del carrito"""
    list_display = (
        'id',
        'get_cart_owner',
        'product',
        'quantity',
        'get_subtotal_display',
        'created_at'
    )
    list_filter = ('created_at', 'updated_at')
    search_fields = ('product__name', 'cart__user__username')
    readonly_fields = ('id', 'created_at', 'updated_at', 'get_subtotal_display')
    
    fieldsets = (
        ('Información del Item', {
            'fields': ('cart', 'product', 'quantity')
        }),
        ('Cálculos', {
            'fields': ('get_subtotal_display',)
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_cart_owner(self, obj):
        if obj.cart.user:
            return obj.cart.user.username
        return "Anónimo"
    get_cart_owner.short_description = "Propietario del Carrito"
    
    def get_subtotal_display(self, obj):
        return f"${obj.get_subtotal():.2f}"
    get_subtotal_display.short_description = "Subtotal"
