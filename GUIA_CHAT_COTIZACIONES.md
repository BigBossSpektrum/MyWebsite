# Guía de Uso - Sistema de Chat para Cotizaciones

## 🚀 Flujo Completo del Sistema

### Para Clientes:

#### 1. Agregar Productos al Carrito
- Navega por el catálogo de productos
- Haz clic en "Agregar al Carrito de Cotización"
- Ajusta las cantidades según necesites

#### 2. Solicitar Cotización
- Ve a tu carrito en `/cart/`
- Revisa los productos agregados
- Haz clic en **"Solicitar Cotización"**
- Si no estás autenticado, se te pedirá iniciar sesión

#### 3. Chatear con el Administrador
- Automáticamente se crea una orden y se abre el chat
- Podrás ver la sala de chat en tiempo real
- Escribe tus preguntas o solicitudes
- El administrador responderá en tiempo real

#### 4. Acceder al Chat Posteriormente
Puedes acceder al chat de varias formas:

**Desde el Historial de Órdenes:**
- Ve a "Mis Pedidos" o `/orders/history/`
- Verás un botón **"Chat"** en órdenes pendientes o en proceso
- Haz clic para acceder a la sala de chat

**Desde los Detalles de una Orden:**
- Entra a cualquier orden pendiente o en proceso
- Verás un banner destacado con el botón **"Abrir Chat"**
- Haz clic para comunicarte con el administrador

**Desde la Lista de Chats:**
- Ve directamente a `/chat/`
- Verás todas tus conversaciones activas
- Podrás ver mensajes no leídos marcados con un badge

---

### Para Administradores:

#### 1. Ver Todas las Órdenes
- Accede al panel de administración de órdenes
- Verás todas las órdenes de todos los clientes

#### 2. Acceder a Chats
**Desde los Detalles de Orden:**
- Haz clic en **"Abrir Chat con Cliente"**
- Se abrirá la sala de chat con ese cliente

**Desde la Lista de Chats:**
- Ve a `/chat/`
- Verás TODOS los chats activos de todos los clientes
- Los mensajes no leídos estarán marcados

#### 3. Gestionar Conversaciones
- Responde a las consultas de clientes en tiempo real
- Proporciona cotizaciones personalizadas
- Negocia precios y condiciones
- Cuando termines, puedes **"Cerrar Chat"**

---

## 📍 URLs Importantes

### Para Clientes:
- **Carrito:** `/cart/`
- **Historial de Órdenes:** `/orders/history/`
- **Mis Chats:** `/chat/`
- **Detalle de Orden:** `/orders/<order_id>/`
- **Chat de una Orden:** `/chat/order/<order_id>/chat/`

### Para Administradores:
- **Lista de Órdenes (Admin):** `/orders/admin/`
- **Todos los Chats:** `/chat/`
- **Detalle de Orden (Admin):** `/orders/admin/<order_id>/`

---

## 💡 Características del Chat

### ✅ Mensajería en Tiempo Real
- Los mensajes se envían y reciben instantáneamente
- No necesitas recargar la página

### ✅ Historial de Mensajes
- Al abrir un chat, se carga automáticamente el historial completo
- Puedes ver todas las conversaciones previas

### ✅ Indicadores de Lectura
- Los mensajes se marcan como leídos automáticamente
- Puedes ver cuántos mensajes no leídos tienes

### ✅ Información de la Orden
- En el chat puedes ver los detalles de la orden
- Lista de productos y cantidades
- Estado actual de la orden

### ✅ Seguridad
- Solo el cliente de la orden y los administradores pueden acceder
- Autenticación requerida
- Conexiones WebSocket seguras

---

## 🔧 Configuración Técnica

### Variables de Entorno Necesarias:
```bash
# En producción, necesitas Redis
REDIS_URL=redis://your-redis-url:6379/0
```

### Para Desarrollo (sin Redis):
El sistema usa `InMemoryChannelLayer` por defecto si no se configura Redis.

### Servidor ASGI:
```bash
# Ejecutar con Daphne
daphne -b 0.0.0.0 -p 8000 Zultech_main.asgi:application

# O con Uvicorn
uvicorn Zultech_main.asgi:application --host 0.0.0.0 --port 8000
```

---

## 🎯 Flujo de Trabajo Recomendado

### Proceso de Cotización:

1. **Cliente agrega productos** → Carrito
2. **Cliente solicita cotización** → Se crea Orden (estado: pending)
3. **Sistema abre chat automáticamente** → Cliente y Admin conectados
4. **Admin proporciona cotización** → Chat en tiempo real
5. **Cliente acepta/negocia** → Conversación continúa
6. **Admin actualiza estado** → processing → shipped → delivered → completed
7. **Chat se cierra** → Cuando la orden está completada o cancelada

---

## 🛠️ Solución de Problemas

### WebSocket no conecta:
- Verifica que estés usando un servidor ASGI (Daphne/Uvicorn)
- Revisa que el puerto sea correcto (8000 por defecto)
- Comprueba la configuración de CHANNEL_LAYERS en settings.py

### Mensajes no se envían:
- Verifica que Redis esté funcionando (en producción)
- Revisa los logs del servidor
- Asegúrate de estar autenticado

### No puedo acceder a un chat:
- Solo el cliente de la orden y admins tienen acceso
- Verifica que la orden exista
- Confirma tu rol de usuario

---

## 📝 Notas Importantes

1. **Autenticación Requerida**: Todos los usuarios deben estar autenticados
2. **Roles**: El sistema diferencia entre clientes (role='customer') y administradores (role='admin')
3. **Una orden = Un chat**: Cada orden tiene su propia sala de chat
4. **Chats activos**: Solo órdenes pendientes o en proceso tienen chats accesibles
5. **Historial permanente**: Los mensajes se guardan en la base de datos

---

## 🔄 Próximas Mejoras Planificadas

- [ ] Notificaciones push para nuevos mensajes
- [ ] Soporte para enviar archivos e imágenes
- [ ] Indicador de "escribiendo..."
- [ ] Búsqueda en historial de mensajes
- [ ] Exportar conversaciones a PDF
- [ ] Respuestas rápidas predefinidas para admins
