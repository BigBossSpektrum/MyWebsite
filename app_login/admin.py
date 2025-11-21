from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.db.models import Count
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    """Administración personalizada de usuarios con funcionalidades avanzadas"""
    list_display = (
        'username',
        'email',
        'full_name',
        'role_colored',
        'is_active',
        'is_staff',
        'orders_count',
        'date_joined'
    )
    list_filter = (
        'role',
        'is_active',
        'is_staff',
        'is_superuser',
        'date_joined',
        'last_login'
    )
    search_fields = ('username', 'email', 'Correo_Electronico', 'first_name', 'last_name', 'Telefono')
    ordering = ('-date_joined',)
    list_per_page = 25
    date_hierarchy = 'date_joined'
    actions = ['activate_users', 'deactivate_users', 'make_clients', 'make_admins', 'delete_selected_users']
    
    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Información Personal', {
            'fields': ('first_name', 'last_name', 'email', 'Correo_Electronico', 'Foto_Perfil', 'Fecha_de_Nacimiento')
        }),
        ('Información de Contacto', {
            'fields': ('Telefono', 'Direccion', 'Ciudad', 'Estado', 'Codigo_Postal'),
        }),
        ('Permisos y Rol', {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser')
        }),
        ('Grupos y Permisos', {
            'fields': ('groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        ('Fechas Importantes', {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',)
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'Correo_Electronico', 'password1', 'password2'),
        }),
        ('Información Personal', {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'Telefono', 'Fecha_de_Nacimiento', 'Foto_Perfil'),
        }),
        ('Información de Contacto', {
            'classes': ('wide',),
            'fields': ('Direccion', 'Ciudad', 'Estado', 'Codigo_Postal'),
        }),
        ('Rol y Permisos', {
            'classes': ('wide',),
            'fields': ('role', 'is_staff', 'is_active'),
        }),
    )
    
    readonly_fields = ('date_joined', 'last_login')
    
    def has_delete_permission(self, request, obj=None):
        """Permite eliminar usuarios y sus objetos relacionados"""
        return request.user.is_superuser
    
    def delete_queryset(self, request, queryset):
        """Elimina múltiples usuarios y sus objetos relacionados"""
        for obj in queryset:
            obj.delete()
    
    def get_queryset(self, request):
        """Optimiza las consultas con annotate"""
        queryset = super().get_queryset(request)
        return queryset.annotate(_orders_count=Count('orders'))
    
    def full_name(self, obj):
        """Muestra el nombre completo del usuario"""
        if obj.first_name and obj.last_name:
            return f"{obj.first_name} {obj.last_name}"
        return "-"
    full_name.short_description = "Nombre Completo"
    
    def role_colored(self, obj):
        """Muestra el rol con colores"""
        colors = {
            'ADMIN': '#dc3545',
            'CUSTOMER': '#28a745',
        }
        color = colors.get(obj.role, '#6c757d')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_role_display()
        )
    role_colored.short_description = 'Rol'
    role_colored.admin_order_field = 'role'
    
    def orders_count(self, obj):
        """Muestra el número de órdenes del usuario"""
        if hasattr(obj, '_orders_count'):
            count = obj._orders_count
        else:
            count = obj.orders.count()
        
        if count == 0:
            return format_html('<span style="color: #888;">0</span>')
        return format_html(
            '<a href="/admin/app_orders/order/?user__id__exact={}">{}</a>',
            obj.id,
            count
        )
    orders_count.short_description = 'Órdenes'
    orders_count.admin_order_field = '_orders_count'
    
    @admin.action(description='Activar usuarios seleccionados')
    def activate_users(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} usuario(s) activado(s).')
    
    @admin.action(description='Desactivar usuarios seleccionados')
    def deactivate_users(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} usuario(s) desactivado(s).')
    
    @admin.action(description='Cambiar rol a Cliente')
    def make_clients(self, request, queryset):
        updated = queryset.update(role='CUSTOMER')
        self.message_user(request, f'{updated} usuario(s) cambiado(s) a Cliente.')
    
    @admin.action(description='Cambiar rol a Administrador')
    def make_admins(self, request, queryset):
        updated = queryset.update(role='ADMIN')
        self.message_user(request, f'{updated} usuario(s) cambiado(s) a Administrador.')
    
    @admin.action(description='Eliminar usuarios seleccionados')
    def delete_selected_users(self, request, queryset):
        """Elimina usuarios y todos sus objetos relacionados"""
        if request.user.is_superuser:
            count = queryset.count()
            for user in queryset:
                user.delete()
            self.message_user(request, f'{count} usuario(s) eliminado(s) junto con sus datos relacionados.')
        else:
            self.message_user(request, 'No tienes permisos para eliminar usuarios.', level='error')

admin.site.register(CustomUser, CustomUserAdmin)
