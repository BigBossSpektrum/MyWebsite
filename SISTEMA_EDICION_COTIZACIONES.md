# Sistema de Edición de Precios para Cotizaciones

## 📝 Descripción

Sistema que permite a los administradores modificar los precios y cantidades de los artículos en las órdenes para crear cotizaciones personalizadas. Los cambios se guardan únicamente en la orden sin afectar los precios originales de los productos en el catálogo.

## ✨ Características Implementadas

### 1. **Vista de Administrador Mejorada**
- Botón "Editar Cotización" en la cabecera
- Tabla con vista de precios originales del producto
- Comparación entre precio original y precio de cotización
- Información de stock disponible

### 2. **Modo de Edición**
- Activación con un clic en el botón "Editar Cotización"
- Campos de entrada para:
  - Precio unitario (con validación de mínimo 0)
  - Cantidad (con validación de mínimo 1)
- Cálculo automático de subtotales
- Cálculo automático del total general

### 3. **Cálculos en Tiempo Real**
- Los subtotales se actualizan al cambiar precio o cantidad
- El total general se recalcula automáticamente
- Visualización inmediata de los cambios

### 4. **Validaciones**
- Precio no puede ser negativo
- Cantidad debe ser al menos 1
- Confirmación antes de guardar
- Mensajes de error claros

### 5. **Seguridad de Datos**
- Los precios originales del catálogo NO se modifican
- Solo se actualizan los `OrderItem` de la orden específica
- Registro de cambios en la base de datos
- Auditoría con timestamps

## 🔧 Componentes Técnicos

### Archivos Modificados:

#### 1. `app_orders/views.py`
```python
@staff_member_required
def admin_update_order_prices(request, order_id):
    """
    Vista para actualizar precios de items
    - Valida datos de entrada
    - Actualiza OrderItems sin tocar productos
    - Recalcula total de la orden
    - Proporciona feedback al usuario
    """
```

**Características:**
- ✅ Validación de tipos de datos (Decimal, int)
- ✅ Validación de valores (no negativos, mínimos)
- ✅ Manejo de excepciones
- ✅ Mensajes informativos
- ✅ Recálculo automático del total

#### 2. `app_orders/urls.py`
```python
path('admin/orders/<uuid:order_id>/update-prices/', 
     views.admin_update_order_prices, 
     name='admin_update_prices')
```

#### 3. `app_orders/templates/orders/admin/order_detail.html`

**Estructura HTML:**
- Formulario con campos para cada item
- Inputs ocultos por defecto (modo vista)
- Botones de acción contextuales
- Alert informativo sobre el comportamiento

**JavaScript:**
- Toggle entre modo vista y edición
- Cálculo automático de subtotales
- Cálculo automático del total
- Validación en cliente
- Confirmación antes de enviar

## 📊 Flujo de Uso

### Para el Administrador:

```
1. Ver orden en panel de administración
   ↓
2. Hacer clic en "Editar Cotización"
   ↓
3. Modificar precios y/o cantidades
   ↓ (automático)
4. Ver actualización de subtotales y total
   ↓
5. Hacer clic en "Guardar Cotización"
   ↓
6. Confirmar cambios
   ↓
7. Sistema guarda y muestra mensaje de éxito
```

### Funciones Disponibles:

#### **Editar Cotización**
- Modifica precio unitario de cualquier item
- Modifica cantidad de cualquier item
- Ve el precio original del producto para referencia

#### **Cancelar Edición**
- Restaura valores originales
- Pide confirmación antes de cancelar
- Recarga la página con datos originales

#### **Guardar Cotización**
- Valida todos los datos
- Pide confirmación
- Guarda cambios en la base de datos
- Muestra el nuevo total

## 💾 Base de Datos

### Modelo `OrderItem`:
```python
class OrderItem(models.Model):
    order = models.ForeignKey(Order, ...)
    product = models.ForeignKey(Product, ...)  # Referencia al producto original
    quantity = models.PositiveIntegerField()   # Cantidad cotizada
    price = models.DecimalField(...)           # Precio cotizado (puede diferir del producto)
    subtotal = models.DecimalField(...)        # Calculado: price * quantity
```

### Modelo `Product`:
El precio del producto **NO se modifica**:
```python
class Product(models.Model):
    name = models.CharField(...)
    price = models.DecimalField(...)  # Precio original - INMUTABLE desde órdenes
    stock = models.IntegerField(...)
```

## 🎯 Casos de Uso

### Caso 1: Descuento por Volumen
```
Producto: Cable HDMI
Precio Original: $15.00
Cantidad: 100 unidades

Cotización:
Precio Unitario: $12.00 (20% descuento)
Cantidad: 100
Subtotal: $1,200.00
```

### Caso 2: Precio Personalizado
```
Producto: Instalación Eléctrica
Precio Original: $500.00
Cantidad: 1

Cotización:
Precio Unitario: $450.00 (negociación)
Cantidad: 1
Subtotal: $450.00
```

### Caso 3: Ajuste de Cantidad
```
Producto: Switch de Red
Precio Original: $80.00
Cantidad Original: 5

Cotización:
Precio Unitario: $80.00 (sin cambio)
Cantidad: 10 (cliente aumentó pedido)
Subtotal: $800.00
```

## ✅ Validaciones Implementadas

### Frontend (JavaScript):
1. ✅ Precio >= 0
2. ✅ Cantidad >= 1
3. ✅ Confirmación antes de guardar
4. ✅ Confirmación antes de cancelar con cambios
5. ✅ Cálculos automáticos correctos

### Backend (Python):
1. ✅ Verificación de tipo Decimal para precios
2. ✅ Verificación de tipo int para cantidades
3. ✅ Validación de valores mínimos
4. ✅ Manejo de excepciones
5. ✅ Mensajes de error específicos
6. ✅ Solo usuarios staff pueden acceder

## 🔒 Seguridad

### Permisos:
- ✅ Solo usuarios con `@staff_member_required`
- ✅ Validación en backend (no se confía solo en frontend)
- ✅ CSRF token en formularios

### Integridad de Datos:
- ✅ Los productos originales NO se modifican
- ✅ Solo se actualizan los OrderItems
- ✅ Transacciones atómicas implícitas
- ✅ Timestamps de auditoría

## 📱 Interfaz de Usuario

### Elementos Visuales:

#### Modo Vista:
- Tabla limpia y legible
- Precios actuales destacados
- Precio original como referencia
- Total destacado en la parte inferior

#### Modo Edición:
- Inputs con formato monetario ($)
- Validación visual
- Colores para diferenciar estados
- Botones de acción claros
- Alert informativo sobre el comportamiento

### Estilos:
```css
- Tabla bordered para claridad
- Thead light para cabecera
- Input groups para precios con $
- Badge warning para stock bajo
- Alert info para instrucciones
- Botones con iconos FontAwesome
```

## 🚀 Ventajas del Sistema

### Para el Negocio:
1. **Flexibilidad en cotizaciones**
   - Descuentos por volumen
   - Precios negociados
   - Ofertas especiales

2. **Historial completo**
   - Registro de cada cotización
   - Auditoría de cambios
   - Trazabilidad

3. **Protección del catálogo**
   - Precios originales intactos
   - No afecta otras órdenes
   - Consistencia en el catálogo

### Para el Administrador:
1. **Interfaz intuitiva**
   - Edición in-place
   - Cálculos automáticos
   - Feedback inmediato

2. **Seguridad**
   - Validaciones múltiples
   - Confirmaciones
   - Prevención de errores

3. **Eficiencia**
   - Proceso rápido
   - Sin necesidad de salir de la página
   - Actualización inmediata

### Para el Cliente:
1. **Transparencia**
   - Ve el precio cotizado
   - Registro permanente
   - Puede ser consultado en chat

2. **Personalización**
   - Precios adaptados a su caso
   - Negociación posible
   - Ofertas específicas

## 📈 Métricas y Reportes

### Datos Disponibles:
- Precio original vs precio cotizado
- Descuentos aplicados
- Total de cotizaciones modificadas
- Historial de cambios por orden

### Análisis Posible:
- Promedio de descuentos otorgados
- Productos con más variación de precio
- Clientes con más cotizaciones personalizadas

## 🎓 Ejemplo de Uso Completo

```
Orden #ABC123
Cliente: cliente@example.com

Productos Originales:
1. Cable Cat6 - $5.00 x 50 = $250.00
2. Switch 24p - $120.00 x 2 = $240.00
3. Instalación - $300.00 x 1 = $300.00
Total Original: $790.00

Admin hace clic en "Editar Cotización"

Modificaciones:
1. Cable Cat6 - $4.50 x 100 = $450.00 (descuento + aumento cantidad)
2. Switch 24p - $110.00 x 2 = $220.00 (descuento)
3. Instalación - $250.00 x 1 = $250.00 (descuento)

Nuevo Total: $920.00

Admin guarda → Cliente ve nueva cotización en chat
```

## ✅ Checklist de Verificación

- [x] Vista creada (`admin_update_order_prices`)
- [x] URL configurada
- [x] Template actualizado
- [x] JavaScript implementado
- [x] Validaciones frontend
- [x] Validaciones backend
- [x] Cálculos automáticos
- [x] Mensajes de feedback
- [x] Protección de datos originales
- [x] Documentación completa

## 🎉 Estado

**✅ IMPLEMENTADO Y FUNCIONAL**

El sistema de edición de precios para cotizaciones está completamente implementado y listo para usar. Los administradores pueden crear cotizaciones personalizadas manteniendo la integridad del catálogo de productos.
