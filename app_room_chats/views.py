from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import ChatRoom, Message
from app_orders.models import Order


@login_required
def chat_room(request, room_id):
    """
    Vista principal del chat - muestra la interfaz de chat
    """
    from django.contrib import messages
    
    chat_room = get_object_or_404(ChatRoom, id=room_id)
    
    # Verificar que el usuario tenga el atributo role
    user_role = getattr(request.user, 'role', None)
    is_admin = user_role == 'admin' or request.user.is_staff or request.user.is_superuser
    
    # Verificar que el usuario tenga acceso
    if chat_room.customer != request.user and not is_admin:
        messages.error(request, 'No tienes permiso para acceder a este chat.')
        return redirect('website:Dashboard')
    
    # Marcar mensajes como leídos
    if is_admin:
        chat_room.messages.filter(sender__role='customer', is_read=False).update(is_read=True)
    else:
        chat_room.messages.filter(sender__role='admin', is_read=False).update(is_read=True)
    
    context = {
        'chat_room': chat_room,
        'order': chat_room.order,
    }
    
    return render(request, 'room_chats/chat_room.html', context)


@login_required
def create_or_get_chat(request, order_id):
    """
    Crear o recuperar sala de chat para una orden específica
    """
    from django.contrib import messages
    
    try:
        order = get_object_or_404(Order, id=order_id)
    except:
        messages.error(request, 'No se encontró la orden especificada.')
        return redirect('orders:order_history')
    
    # Verificar que el usuario tenga el atributo role
    user_role = getattr(request.user, 'role', None)
    
    # Verificar que el usuario sea el dueño de la orden o un admin
    is_admin = user_role == 'admin' or request.user.is_staff or request.user.is_superuser
    
    if order.user != request.user and not is_admin:
        messages.error(request, 'No tienes permiso para acceder a este chat.')
        return redirect('website:Dashboard')
    
    # Buscar o crear la sala de chat
    chat_room, created = ChatRoom.objects.get_or_create(
        order=order,
        defaults={
            'customer': order.user,
            'admin': None  # Se asignará cuando un admin entre
        }
    )
    
    # Si es un admin entrando, asignarlo
    if is_admin and not chat_room.admin:
        chat_room.admin = request.user
        chat_room.save()
    
    if created:
        messages.success(request, 'Sala de chat creada exitosamente.')
    
    return redirect('room_chats:chat_room', room_id=chat_room.id)


@login_required
def chat_list(request):
    """
    Lista de todas las salas de chat del usuario
    """
    # Verificar que el usuario tenga el atributo role
    user_role = getattr(request.user, 'role', None)
    is_admin = user_role == 'admin' or request.user.is_staff or request.user.is_superuser
    
    if is_admin:
        # Admins ven todas las salas
        chat_rooms = ChatRoom.objects.filter(is_active=True).select_related(
            'order', 'customer', 'admin'
        ).prefetch_related('messages', 'order__items')
        
        # Aplicar filtros
        status_filter = request.GET.get('status', '')
        assigned_filter = request.GET.get('assigned', '')
        search_query = request.GET.get('search', '')
        
        if status_filter:
            chat_rooms = chat_rooms.filter(order__status=status_filter)
        
        if assigned_filter == 'yes':
            chat_rooms = chat_rooms.filter(admin__isnull=False)
        elif assigned_filter == 'no':
            chat_rooms = chat_rooms.filter(admin__isnull=True)
        
        if search_query:
            from django.db.models import Q
            chat_rooms = chat_rooms.filter(
                Q(customer__email__icontains=search_query) |
                Q(order__id__icontains=search_query)
            )
        
        # Estadísticas para admins (sin filtros)
        all_chats = ChatRoom.objects.filter(is_active=True)
        total_chats = all_chats.count()
        unassigned_chats = all_chats.filter(admin__isnull=True).count()
        pending_orders = all_chats.filter(order__status='pending').count()
        processing_orders = all_chats.filter(order__status='processing').count()
        
        # Contar mensajes no leídos totales
        total_unread = 0
        for chat in all_chats.prefetch_related('messages'):
            total_unread += chat.unread_count_for_admin
        
        context = {
            'chat_rooms': chat_rooms,
            'total_chats': total_chats,
            'unassigned_chats': unassigned_chats,
            'pending_orders': pending_orders,
            'processing_orders': processing_orders,
            'total_unread': total_unread,
            'status_filter': status_filter,
            'assigned_filter': assigned_filter,
            'search_query': search_query,
        }
    else:
        # Clientes ven solo sus chats
        chat_rooms = ChatRoom.objects.filter(
            customer=request.user, 
            is_active=True
        ).select_related('order', 'admin').prefetch_related('messages', 'order__items')
        
        context = {
            'chat_rooms': chat_rooms,
        }
    
    return render(request, 'room_chats/chat_list.html', context)


@login_required
@require_http_methods(["POST"])
def close_chat(request, room_id):
    """
    Cerrar una sala de chat (solo admin)
    """
    # Verificar que el usuario tenga el atributo role
    user_role = getattr(request.user, 'role', None)
    is_admin = user_role == 'admin' or request.user.is_staff or request.user.is_superuser
    
    if not is_admin:
        return JsonResponse({'error': 'Sin permisos'}, status=403)
    
    chat_room = get_object_or_404(ChatRoom, id=room_id)
    chat_room.is_active = False
    chat_room.save()
    
    return JsonResponse({'success': True, 'message': 'Chat cerrado'})
