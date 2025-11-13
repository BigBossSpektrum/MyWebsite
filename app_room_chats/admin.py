from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count, Max, Q
from .models import ChatRoom, Message


class MessageInline(admin.TabularInline):
    """Inline para mostrar mensajes en la sala de chat"""
    model = Message
    extra = 0
    fields = ('sender', 'content_preview', 'is_read', 'created_at')
    readonly_fields = ('sender', 'content_preview', 'is_read', 'created_at')
    can_delete = False
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Mensaje'
    
    def has_add_permission(self, request, obj=None):
        return False


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    """Administración de salas de chat con funcionalidades avanzadas"""
    list_display = (
        'id',
        'order',
        'customer',
        'admin',
        'status_colored',
        'messages_count',
        'unread_messages',
        'last_message_time',
        'created_at'
    )
    list_filter = (
        'is_active',
        'created_at',
        'updated_at',
        ('admin', admin.EmptyFieldListFilter)
    )
    search_fields = ('customer__email', 'customer__username', 'admin__email', 'admin__username', 'order__id', 'id')
    readonly_fields = ('id', 'created_at', 'updated_at', 'messages_count', 'unread_messages', 'last_message_time')
    list_per_page = 25
    date_hierarchy = 'created_at'
    inlines = [MessageInline]
    actions = ['activate_rooms', 'deactivate_rooms', 'mark_all_as_read']
    
    fieldsets = (
        ('Información General', {
            'fields': ('id', 'order', 'customer', 'admin', 'is_active')
        }),
        ('Estadísticas', {
            'fields': ('messages_count', 'unread_messages', 'last_message_time')
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """Optimiza las consultas con select_related y annotate"""
        queryset = super().get_queryset(request)
        return queryset.select_related('order', 'customer', 'admin').annotate(
            _messages_count=Count('messages'),
            _unread_count=Count('messages', filter=Q(messages__is_read=False)),
            _last_message_time=Max('messages__created_at')
        )
    
    def status_colored(self, obj):
        """Muestra el estado con colores"""
        if obj.is_active:
            return format_html(
                '<span style="color: #28a745; font-weight: bold;">✓ Activo</span>'
            )
        return format_html(
            '<span style="color: #dc3545; font-weight: bold;">✗ Inactivo</span>'
        )
    status_colored.short_description = 'Estado'
    status_colored.admin_order_field = 'is_active'
    
    def messages_count(self, obj):
        """Muestra el número de mensajes"""
        if hasattr(obj, '_messages_count'):
            count = obj._messages_count
        else:
            count = obj.messages.count()
        
        if count == 0:
            return format_html('<span style="color: #888;">0</span>')
        return format_html('<strong>{}</strong>', count)
    messages_count.short_description = 'Mensajes'
    messages_count.admin_order_field = '_messages_count'
    
    def unread_messages(self, obj):
        """Muestra el número de mensajes no leídos"""
        if hasattr(obj, '_unread_count'):
            count = obj._unread_count
        else:
            count = obj.messages.filter(is_read=False).count()
        
        if count == 0:
            return format_html('<span style="color: #888;">0</span>')
        return format_html('<span style="color: #dc3545; font-weight: bold;">{}</span>', count)
    unread_messages.short_description = 'No Leídos'
    unread_messages.admin_order_field = '_unread_count'
    
    def last_message_time(self, obj):
        """Muestra la hora del último mensaje"""
        if hasattr(obj, '_last_message_time'):
            last_time = obj._last_message_time
        else:
            last_message = obj.messages.order_by('-created_at').first()
            last_time = last_message.created_at if last_message else None
        
        if last_time:
            return last_time.strftime('%d/%m/%Y %H:%M')
        return format_html('<span style="color: #888;">Sin mensajes</span>')
    last_message_time.short_description = 'Último Mensaje'
    last_message_time.admin_order_field = '_last_message_time'
    
    @admin.action(description='Activar salas seleccionadas')
    def activate_rooms(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} sala(s) activada(s).')
    
    @admin.action(description='Desactivar salas seleccionadas')
    def deactivate_rooms(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} sala(s) desactivada(s).')
    
    @admin.action(description='Marcar todos los mensajes como leídos')
    def mark_all_as_read(self, request, queryset):
        total_updated = 0
        for room in queryset:
            total_updated += room.messages.filter(is_read=False).update(is_read=True)
        self.message_user(request, f'{total_updated} mensaje(s) marcado(s) como leído.')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """Administración de mensajes con funcionalidades mejoradas"""
    list_display = (
        'id',
        'chat_room',
        'sender',
        'content_preview',
        'read_status',
        'created_at'
    )
    list_filter = (
        'is_read',
        'created_at',
        'sender__role'
    )
    search_fields = ('sender__email', 'sender__username', 'content', 'chat_room__id')
    readonly_fields = ('id', 'created_at', 'chat_room', 'sender', 'content')
    list_per_page = 50
    date_hierarchy = 'created_at'
    actions = ['mark_as_read', 'mark_as_unread']
    
    fieldsets = (
        ('Información del Mensaje', {
            'fields': ('id', 'chat_room', 'sender', 'content', 'is_read')
        }),
        ('Fechas', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """Optimiza las consultas con select_related"""
        queryset = super().get_queryset(request)
        return queryset.select_related('chat_room', 'chat_room__order', 'sender')
    
    def content_preview(self, obj):
        """Muestra una vista previa del contenido"""
        preview = obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
        return format_html('<span title="{}">{}</span>', obj.content, preview)
    content_preview.short_description = 'Mensaje'
    
    def read_status(self, obj):
        """Muestra el estado de lectura con iconos"""
        if obj.is_read:
            return format_html('<span style="color: #28a745;">✓ Leído</span>')
        return format_html('<span style="color: #ffc107;">⚠ No leído</span>')
    read_status.short_description = 'Estado'
    read_status.admin_order_field = 'is_read'
    
    @admin.action(description='Marcar como leído')
    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} mensaje(s) marcado(s) como leído.')
    
    @admin.action(description='Marcar como no leído')
    def mark_as_unread(self, request, queryset):
        updated = queryset.update(is_read=False)
        self.message_user(request, f'{updated} mensaje(s) marcado(s) como no leído.')
    
    def has_add_permission(self, request):
        """No permitir agregar mensajes manualmente desde el admin"""
        return False
    
    def has_delete_permission(self, request, obj=None):
        """Solo superusuarios pueden eliminar mensajes"""
        return request.user.is_superuser
