from django import template

register = template.Library()


@register.filter
def is_admin(user):
    """
    Verifica si un usuario es administrador de forma robusta
    """
    if not user or not user.is_authenticated:
        return False
    
    # Verificar múltiples formas de ser admin
    user_role = getattr(user, 'role', None)
    return user_role == 'admin' or user.is_staff or user.is_superuser


@register.filter
def get_user_role(user):
    """
    Obtiene el role del usuario de forma segura
    """
    if not user or not user.is_authenticated:
        return 'guest'
    
    return getattr(user, 'role', 'customer')
