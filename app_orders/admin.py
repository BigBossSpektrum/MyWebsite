from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from django.db.models import Sum, Count, Q
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    """Inline para mostrar los items de la orden"""
    model = OrderItem
    extra = 0
    readonly_fields = ('id', 'product', 'quantity', 'price', 'subtotal')
    can_delete = False
    
    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Administración de órdenes con funcionalidades avanzadas"""
    list_display = (
        'id',
        'user',
        'status_colored',
        'total_formatted',
        'items_count',
        'created_at',
        'updated_at'
    )
    list_filter = (
        'status',
        'created_at',
        'updated_at',
        ('completed_at', admin.EmptyFieldListFilter),
        ('cancelled_at', admin.EmptyFieldListFilter)
    )
    search_fields = ('id', 'user__username', 'user__email', 'user__first_name', 'user__last_name')
    readonly_fields = (
        'id',
        'created_at',
        'updated_at',
        'completed_at',
        'cancelled_at',
        'items_count',
        'total_formatted'
    )
    list_per_page = 25
    date_hierarchy = 'created_at'
    inlines = [OrderItemInline]
    actions = ['mark_as_processing', 'mark_as_shipped', 'mark_as_delivered', 'mark_as_completed', 'cancel_orders']
    
    fieldsets = (
        ('Información de la Orden', {
            'fields': ('id', 'user', 'status', 'total')
        }),
        ('Estadísticas', {
            'fields': ('items_count', 'total_formatted')
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at', 'completed_at', 'cancelled_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """Optimiza las consultas con select_related y annotate"""
        queryset = super().get_queryset(request)
        return queryset.select_related('user').annotate(
            _items_count=Count('items')
        )
    
    def status_colored(self, obj):
        """Muestra el estado con colores"""
        colors = {
            'pending': '#FFA500',
            'processing': '#1E90FF',
            'shipped': '#9370DB',
            'delivered': '#32CD32',
            'completed': '#228B22',
            'cancelled': '#DC143C',
        }
        color = colors.get(obj.status, '#808080')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_colored.short_description = 'Estado'
    status_colored.admin_order_field = 'status'
    
    def total_formatted(self, obj):
        """Formatea el total con símbolo de moneda"""
        return format_html('<strong>${}</strong>', f"{obj.total:.2f}")
    total_formatted.short_description = 'Total'
    total_formatted.admin_order_field = 'total'
    
    def items_count(self, obj):
        """Muestra el número de items en la orden"""
        if hasattr(obj, '_items_count'):
            return obj._items_count
        return obj.items.count()
    items_count.short_description = 'Items'
    items_count.admin_order_field = '_items_count'
    
    # Acciones personalizadas
    @admin.action(description='Marcar como En Proceso')
    def mark_as_processing(self, request, queryset):
        updated = queryset.filter(status='pending').update(status='processing')
        self.message_user(request, f'{updated} orden(es) marcada(s) como En Proceso.')
    
    @admin.action(description='Marcar como Enviado')
    def mark_as_shipped(self, request, queryset):
        updated = queryset.filter(status__in=['pending', 'processing']).update(status='shipped')
        self.message_user(request, f'{updated} orden(es) marcada(s) como Enviado.')
    
    @admin.action(description='Marcar como Entregado')
    def mark_as_delivered(self, request, queryset):
        updated = queryset.filter(status='shipped').update(status='delivered')
        self.message_user(request, f'{updated} orden(es) marcada(s) como Entregado.')
    
    @admin.action(description='Marcar como Completado')
    def mark_as_completed(self, request, queryset):
        updated = queryset.filter(status='delivered').update(
            status='completed',
            completed_at=timezone.now()
        )
        self.message_user(request, f'{updated} orden(es) marcada(s) como Completado.')
    
    @admin.action(description='Cancelar órdenes')
    def cancel_orders(self, request, queryset):
        updated = queryset.filter(status='pending').update(
            status='cancelled',
            cancelled_at=timezone.now()
        )
        self.message_user(request, f'{updated} orden(es) cancelada(s).')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """Administración de items de órdenes"""
    list_display = (
        'id',
        'order',
        'product',
        'quantity',
        'price_formatted',
        'subtotal_formatted'
    )
    list_filter = ('order__status', 'order__created_at')
    search_fields = ('order__id', 'product__name', 'order__user__email')
    readonly_fields = ('id', 'order', 'product', 'quantity', 'price', 'subtotal')
    
    fieldsets = (
        ('Información del Item', {
            'fields': ('id', 'order', 'product', 'quantity')
        }),
        ('Precios', {
            'fields': ('price', 'subtotal')
        }),
    )
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def get_queryset(self, request):
        """Optimiza las consultas con select_related"""
        queryset = super().get_queryset(request)
        return queryset.select_related('order', 'order__user', 'product')
    
    def price_formatted(self, obj):
        return f"${obj.price:.2f}"
    price_formatted.short_description = 'Precio'
    price_formatted.admin_order_field = 'price'
    
    def subtotal_formatted(self, obj):
        return format_html('<strong>${}</strong>', f"{obj.subtotal:.2f}")
    subtotal_formatted.short_description = 'Subtotal'
    subtotal_formatted.admin_order_field = 'subtotal'
