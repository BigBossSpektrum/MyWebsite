# Sistema de Chat en Tiempo Real - app_room_chats

## Descripción
Sistema de chat en tiempo real utilizando Django Channels y WebSocket para comunicación entre clientes y administradores sobre órdenes/cotizaciones.

## Características Implementadas

### Modelos
- **ChatRoom**: Sala de chat vinculada a una orden específica
  - Relación uno-a-uno con Order
  - Vincula cliente y administrador
  - Control de estado activo/inactivo
  - Contador de mensajes no leídos

- **Message**: Mensajes individuales en la sala
  - Contenido del mensaje
  - Estado de lectura
  - Timestamp de creación

### WebSocket Consumer
- `ChatConsumer`: Maneja conexiones WebSocket en tiempo real
  - Verificación de autenticación
  - Verificación de permisos de acceso
  - Historial de mensajes al conectar
  - Envío/recepción de mensajes en tiempo real
  - Marcado de mensajes como leídos

### Vistas HTTP
- `chat_room`: Vista principal del chat
- `create_or_get_chat`: Crear o recuperar sala de chat para una orden
- `chat_list`: Lista de chats del usuario
- `close_chat`: Cerrar sala de chat (solo admin)

### URLs
- `/chat/` - Lista de chats
- `/chat/<room_id>/` - Sala de chat específica
- `/chat/order/<order_id>/chat/` - Crear/acceder chat de una orden
- `/chat/<room_id>/close/` - Cerrar chat

### WebSocket URLs
- `ws://localhost:8000/ws/chat/<room_id>/` - Conexión WebSocket al chat

## Instalación

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2. Configurar Redis (requerido para producción)
```bash
# Instalar Redis localmente o usar servicio cloud
# Configurar REDIS_URL en variables de entorno
```

### 3. Ejecutar migraciones
```bash
python manage.py makemigrations app_room_chats
python manage.py migrate
```

### 4. Ejecutar servidor ASGI
```bash
# Para desarrollo (con Redis)
daphne -b 0.0.0.0 -p 8000 Zultech_main.asgi:application

# O usar uvicorn
uvicorn Zultech_main.asgi:application --host 0.0.0.0 --port 8000
```

## Uso

### Para Clientes
1. Acceder a una orden desde el panel de órdenes
2. Hacer clic en "Iniciar Chat" o similar
3. Chatear con el administrador en tiempo real

### Para Administradores
1. Ver lista de todos los chats activos en `/chat/`
2. Acceder a cualquier chat
3. Responder a clientes
4. Cerrar chats cuando estén resueltos

## Configuración de Producción

### Variables de Entorno
```
REDIS_URL=redis://your-redis-url:6379/0
```

### Alternativa sin Redis (desarrollo)
Si no tienes Redis, puedes usar InMemoryChannelLayer (solo desarrollo):
```python
# En settings.py
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}
```

⚠️ **Nota**: InMemoryChannelLayer NO debe usarse en producción con múltiples workers.

## Seguridad
- Autenticación requerida para todas las conexiones
- Verificación de permisos por sala
- Solo el cliente de la orden y admins pueden acceder
- CSRF protection en requests HTTP

## Próximas Mejoras
- [ ] Notificaciones push cuando llegan mensajes
- [ ] Soporte para archivos adjuntos
- [ ] Historial completo de mensajes con paginación
- [ ] Indicador de "escribiendo..."
- [ ] Múltiples admins por chat
