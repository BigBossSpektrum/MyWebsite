from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Sum, Count, F
from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    """Inline para mostrar los items del carrito"""
    model = CartItem
    extra = 0
    readonly_fields = ('created_at', 'updated_at', 'get_subtotal_display')
    fields = ('product', 'quantity', 'get_subtotal_display', 'created_at')
    can_delete = True
    
    def get_subtotal_display(self, obj):
        if obj.id:
            return f"${obj.get_subtotal():.2f}"
        return "-"
    get_subtotal_display.short_description = "Subtotal"


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """Administración de carritos con funcionalidades avanzadas"""
    list_display = (
        'id',
        'get_owner',
        'get_total_items_display',
        'get_total_display',
        'is_anonymous',
        'updated_at',
        'created_at'
    )
    list_filter = (
        ('user', admin.EmptyFieldListFilter),
        'created_at',
        'updated_at'
    )
    search_fields = ('user__username', 'user__email', 'session_key', 'id')
    readonly_fields = ('id', 'created_at', 'updated_at', 'get_total_display', 'get_total_items_display')
    inlines = [CartItemInline]
    actions = ['clear_empty_carts', 'clear_old_carts']
    list_per_page = 25
    date_hierarchy = 'created_at'
    
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
    
    def get_queryset(self, request):
        """Optimiza las consultas con select_related y prefetch_related"""
        queryset = super().get_queryset(request)
        return queryset.select_related('user').prefetch_related('items__product')
    
    def get_owner(self, obj):
        if obj.user:
            return format_html(
                '<strong>{}</strong> ({})',
                obj.user.username,
                obj.user.email
            )
        return format_html(
            '<span style="color: #888;">Anónimo ({}...)</span>',
            obj.session_key[:8] if obj.session_key else 'Sin sesión'
        )
    get_owner.short_description = "Propietario"
    
    def is_anonymous(self, obj):
        return obj.user is None
    is_anonymous.boolean = True
    is_anonymous.short_description = "Anónimo"
    
    def get_total_items_display(self, obj):
        count = obj.get_total_items()
        if count == 0:
            return format_html('<span style="color: #888;">0</span>')
        return format_html('<strong>{}</strong>', count)
    get_total_items_display.short_description = "Items"
    
    def get_total_display(self, obj):
        total = obj.get_total()
        if total == 0:
            return format_html('<span style="color: #888;">$0.00</span>')
        return format_html('<strong style="color: #2e7d32;">${}</strong>', f"{total:.2f}")
    get_total_display.short_description = "Total"
    
    @admin.action(description='Limpiar carritos vacíos')
    def clear_empty_carts(self, request, queryset):
        empty_carts = queryset.annotate(items_count=Count('items')).filter(items_count=0)
        count = empty_carts.count()
        empty_carts.delete()
        self.message_user(request, f'{count} carrito(s) vacío(s) eliminado(s).')
    
    @admin.action(description='Limpiar carritos antiguos (>30 días)')
    def clear_old_carts(self, request, queryset):
        from django.utils import timezone
        from datetime import timedelta
        thirty_days_ago = timezone.now() - timedelta(days=30)
        old_carts = queryset.filter(updated_at__lt=thirty_days_ago)
        count = old_carts.count()
        old_carts.delete()
        self.message_user(request, f'{count} carrito(s) antiguo(s) eliminado(s).')


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    """Administración de items del carrito"""
    list_display = (
        'id',
        'get_cart_owner',
        'product',
        'quantity',
        'get_price_display',
        'get_subtotal_display',
        'created_at'
    )
    list_filter = (
        'created_at',
        'updated_at',
        'product__category'
    )
    search_fields = ('product__name', 'cart__user__username', 'cart__user__email')
    readonly_fields = ('id', 'created_at', 'updated_at', 'get_price_display', 'get_subtotal_display')
    list_per_page = 25
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Información del Item', {
            'fields': ('cart', 'product', 'quantity')
        }),
        ('Cálculos', {
            'fields': ('get_price_display', 'get_subtotal_display')
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """Optimiza las consultas con select_related"""
        queryset = super().get_queryset(request)
        return queryset.select_related('cart__user', 'product', 'product__category')
    
    def get_cart_owner(self, obj):
        if obj.cart.user:
            return format_html(
                '<a href="/admin/app_cart/cart/{}/change/">{}</a>',
                obj.cart.id,
                obj.cart.user.username
            )
        return format_html(
            '<span style="color: #888;"><a href="/admin/app_cart/cart/{}/change/">Anónimo</a></span>',
            obj.cart.id
        )
    get_cart_owner.short_description = "Propietario"
    
    def get_price_display(self, obj):
        return f"${obj.product.price:.2f}" if obj.product else "N/A"
    get_price_display.short_description = "Precio Unit."
    
    def get_subtotal_display(self, obj):
        return format_html('<strong>${}</strong>', f"{obj.get_subtotal():.2f}")
    get_subtotal_display.short_description = "Subtotal"
