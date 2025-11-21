from .models import ChatRoom


def unread_chat_count(request):
    """
    Context processor para agregar el contador de mensajes sin leer
    en el menú de navegación para administradores
    """
    if request.user.is_authenticated:
        # Verificar si es admin
        user_role = getattr(request.user, 'role', None)
        is_admin = user_role == 'admin' or request.user.is_staff or request.user.is_superuser
        
        if is_admin:
            try:
                # Obtener todas las salas activas
                chat_rooms = ChatRoom.objects.filter(is_active=True).prefetch_related('messages')
                
                # Contar mensajes no leídos
                total_unread = 0
                for chat in chat_rooms:
                    total_unread += chat.unread_count_for_admin
                
                return {
                    'admin_unread_chats': total_unread
                }
            except Exception:
                pass
    
    return {
        'admin_unread_chats': 0
    }
