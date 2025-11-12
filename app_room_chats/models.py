from django.db import models
from django.contrib.auth import get_user_model
from app_orders.models import Order
import uuid

User = get_user_model()

class ChatRoom(models.Model):
    """
    Sala de chat entre cliente y administrador para discutir una orden/cotización
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='chat_room')
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer_chats')
    admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='admin_chats')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"Chat para Orden {self.order.id}"
    
    @property
    def room_name(self):
        """Nombre único de la sala para WebSocket"""
        return f"chat_{self.id}"
    
    @property
    def unread_count_for_customer(self):
        """Cuenta mensajes no leídos por el cliente"""
        return self.messages.filter(sender__role='admin', is_read=False).count()
    
    @property
    def unread_count_for_admin(self):
        """Cuenta mensajes no leídos por el admin"""
        return self.messages.filter(sender__role='customer', is_read=False).count()


class Message(models.Model):
    """
    Mensaje individual dentro de una sala de chat
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.sender.email}: {self.content[:50]}"
