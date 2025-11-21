import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import ChatRoom, Message

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    """
    Consumer para manejar conexiones WebSocket del chat en tiempo real
    """
    
    async def connect(self):
        """Cuando un usuario se conecta al WebSocket"""
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'
        self.user = self.scope['user']
        
        # Verificar que el usuario esté autenticado
        if not self.user.is_authenticated:
            await self.close()
            return
        
        # Verificar que el usuario tenga acceso a esta sala
        has_access = await self.check_room_access()
        if not has_access:
            await self.close()
            return
        
        # Unirse al grupo de la sala
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Enviar historial de mensajes
        messages = await self.get_messages()
        await self.send(text_data=json.dumps({
            'type': 'message_history',
            'messages': messages
        }))
    
    async def disconnect(self, close_code):
        """Cuando un usuario se desconecta del WebSocket"""
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        """Cuando se recibe un mensaje del WebSocket"""
        text_data_json = json.loads(text_data)
        message_type = text_data_json.get('type', 'chat_message')
        
        if message_type == 'chat_message':
            message_content = text_data_json['message']
            
            # Guardar el mensaje en la base de datos
            message = await self.save_message(message_content)
            
            # Obtener role del usuario
            user_role = getattr(self.user, 'role', 'customer')
            
            # Enviar mensaje a todos en el grupo
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message_content,
                    'sender': self.user.email,
                    'sender_role': user_role,
                    'message_id': str(message.id),
                    'timestamp': message.created_at.isoformat()
                }
            )
        
        elif message_type == 'mark_as_read':
            # Marcar mensajes como leídos
            await self.mark_messages_as_read()
    
    async def chat_message(self, event):
        """Enviar mensaje al WebSocket"""
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': event['message'],
            'sender': event['sender'],
            'sender_role': event['sender_role'],
            'message_id': event['message_id'],
            'timestamp': event['timestamp']
        }))
    
    @database_sync_to_async
    def check_room_access(self):
        """Verificar que el usuario tenga acceso a la sala"""
        try:
            chat_room = ChatRoom.objects.get(id=self.room_id)
            # Verificar role del usuario
            user_role = getattr(self.user, 'role', None)
            is_admin = user_role == 'admin' or self.user.is_staff or self.user.is_superuser
            # El usuario debe ser el cliente de la orden o un admin
            return (chat_room.customer == self.user or is_admin)
        except ChatRoom.DoesNotExist:
            return False
    
    @database_sync_to_async
    def get_messages(self):
        """Obtener el historial de mensajes de la sala"""
        try:
            chat_room = ChatRoom.objects.get(id=self.room_id)
            messages = chat_room.messages.all()[:50]  # Últimos 50 mensajes
            return [
                {
                    'id': str(msg.id),
                    'sender': msg.sender.email,
                    'sender_role': msg.sender.role,
                    'content': msg.content,
                    'timestamp': msg.created_at.isoformat(),
                    'is_read': msg.is_read
                }
                for msg in messages
            ]
        except ChatRoom.DoesNotExist:
            return []
    
    @database_sync_to_async
    def save_message(self, content):
        """Guardar un mensaje en la base de datos"""
        chat_room = ChatRoom.objects.get(id=self.room_id)
        message = Message.objects.create(
            chat_room=chat_room,
            sender=self.user,
            content=content
        )
        return message
    
    @database_sync_to_async
    def mark_messages_as_read(self):
        """Marcar todos los mensajes de otros usuarios como leídos"""
        chat_room = ChatRoom.objects.get(id=self.room_id)
        chat_room.messages.exclude(sender=self.user).update(is_read=True)
