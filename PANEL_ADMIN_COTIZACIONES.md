# Panel de Administración de Cotizaciones

## 📊 Vista General del Panel

El panel de administración de cotizaciones proporciona una interfaz completa para gestionar todas las conversaciones con clientes sobre órdenes y cotizaciones.

## 🔑 Acceso al Panel

### Opciones de Acceso:

1. **Desde el menú de navegación principal:**
   - Opción "Cotizaciones" (icono de chat verde)
   - URL directa: `/chat/`

2. **Desde el panel de órdenes:**
   - Botón "Gestionar Cotizaciones (Chat)" en la parte superior
   - URL: `/orders/admin/`

3. **Desde detalles de una orden:**
   - Botón "Abrir Chat con Cliente"
   - Aparece en cada orden individual

## 📈 Panel de Estadísticas

El panel muestra 4 métricas principales:

### 1. **Chats Activos** (Azul)
- Total de conversaciones activas
- Incluye todas las órdenes con chat habilitado

### 2. **Mensajes Sin Leer** (Rojo)
- Cantidad total de mensajes de clientes no leídos
- Requiere atención inmediata

### 3. **Sin Asignar** (Amarillo)
- Chats que no tienen un administrador asignado
- Nuevas consultas que necesitan atención

### 4. **Pendientes** (Azul claro)
- Órdenes en estado "Pendiente"
- Requieren cotización o respuesta

## 🔍 Sistema de Filtros

### Filtros Disponibles:

#### 1. **Estado de Orden**
Filtra por el estado actual de la orden:
- Pendiente
- En Proceso
- Enviado
- Entregado

#### 2. **Asignación**
- **Asignados**: Chats que ya tienen un admin asignado
- **Sin Asignar**: Chats que necesitan ser asignados

#### 3. **Búsqueda**
Buscar por:
- Email del cliente
- ID de la orden

### Uso de Filtros:
1. Selecciona los criterios deseados
2. Haz clic en "Filtrar"
3. Para limpiar, usa el botón "Limpiar Filtros"

## 📋 Lista de Chats

Cada chat muestra:

### Información Visible:
- **Número de Orden**: ID único de la orden
- **Estado**: Badge con color según el estado
- **Mensajes Nuevos**: Badge rojo/azul con cantidad
- **Cliente**: Email del cliente
- **Admin Asignado**: Quién está atendiendo (o "Sin asignar")
- **Total**: Monto total de la orden
- **Productos**: Cantidad de productos en la orden
- **Fecha de Creación**: Cuándo se creó la orden
- **Última Actividad**: Última vez que hubo actividad en el chat

### Indicadores Visuales:

#### Bordes de Color:
- **Rojo**: Tiene mensajes sin leer de clientes
- **Azul**: Para clientes, mensajes sin leer del admin
- **Sin color**: Sin mensajes pendientes

#### Estados de Orden:
- **Amarillo**: Pendiente
- **Azul**: En Proceso
- **Verde**: Completado
- **Gris**: Otros estados

## 🎯 Flujo de Trabajo Recomendado

### Para Nuevas Cotizaciones:

1. **Ver chats sin asignar** (filtro)
2. **Abrir chat** haciendo clic
3. **Automáticamente te asignas** al entrar
4. **Revisar productos** de la orden
5. **Proporcionar cotización** en tiempo real
6. **Actualizar estado** de la orden según progreso

### Para Chats Existentes:

1. **Priorizar mensajes sin leer** (badge rojo)
2. **Responder consultas**
3. **Actualizar estado** si es necesario
4. **Cerrar chat** cuando se complete la orden

## 💡 Mejores Prácticas

### ✅ Recomendaciones:

1. **Revisa regularmente** los chats sin asignar
2. **Responde rápidamente** los mensajes sin leer
3. **Usa filtros** para organizar tu trabajo
4. **Actualiza estados** de órdenes para reflejar el progreso
5. **Cierra chats** cuando se completen las órdenes

### ⚠️ Puntos Importantes:

- **Auto-asignación**: Al entrar a un chat sin asignar, se te asigna automáticamente
- **Tiempo real**: Los mensajes se envían y reciben instantáneamente
- **Historial completo**: Puedes ver todo el historial de conversación
- **Información contextual**: La orden completa está visible en el chat

## 🛠️ Acciones Disponibles

### En la Lista:
- **Filtrar** chats por múltiples criterios
- **Ver estadísticas** generales
- **Acceso rápido** a cada chat

### Dentro del Chat:
- **Ver orden completa**: Productos, cantidades, totales
- **Chatear en tiempo real**: Respuesta instantánea
- **Cerrar chat**: Cuando la conversación termine
- **Ver detalles de orden**: Link a la vista completa de la orden

## 📊 Interpretación de Estadísticas

### Escenarios Comunes:

#### Alta cantidad de "Sin Asignar":
- Necesitas más admins revisando chats
- Nuevas consultas entrando rápidamente

#### Muchos "Mensajes Sin Leer":
- Clientes esperando respuesta
- Prioridad: responder estos primero

#### Muchas órdenes "Pendientes":
- Cotizaciones esperando procesamiento
- Convertir a "En Proceso" tras cotizar

## 🔄 Estados de Orden y Chats

### Relación:

```
Pendiente → Cliente solicita cotización
    ↓
En Proceso → Admin proporciona cotización
    ↓
Enviado → Productos en camino
    ↓
Entregado → Cliente recibió productos
    ↓
Completado → Proceso finalizado (chat se puede cerrar)
```

## 📞 Soporte y Ayuda

### Si tienes problemas:

1. **WebSocket no conecta**: Verifica servidor ASGI
2. **No ves mensajes**: Revisa permisos de usuario
3. **Filtros no funcionan**: Limpia filtros y reintenta
4. **Estadísticas incorrectas**: Refresca la página

## 🔐 Seguridad y Permisos

- Solo usuarios con `role='admin'` ven el panel completo
- Los clientes solo ven sus propios chats
- Cada chat verifica permisos antes de mostrar contenido
- Las estadísticas solo son visibles para administradores

---

## 📱 Acceso Móvil

El panel es completamente responsive y funciona en:
- 📱 Smartphones
- 💻 Tablets
- 🖥️ Escritorio

Los chats en tiempo real funcionan en todos los dispositivos con soporte WebSocket.
