# App Cart - Sistema CRUD de Carrito de Compras

## Descripción
Sistema completo de carrito de compras con operaciones CRUD (Create, Read, Update, Delete) implementado con modelos de base de datos en Django.

## Modelos

### Cart (Carrito)
Representa el carrito de compras de un usuario o sesión anónima.

**Campos:**
- `id`: UUID único del carrito
- `user`: Usuario propietario (nullable para carritos anónimos)
- `session_key`: Clave de sesión para usuarios anónimos
- `created_at`: Fecha de creación
- `updated_at`: Fecha de última actualización

**Métodos:**
- `get_total()`: Calcula el total del carrito
- `get_total_items()`: Obtiene el número total de artículos
- `clear()`: Limpia todos los items del carrito

### CartItem (Item del Carrito)
Representa un producto individual en el carrito.

**Campos:**
- `id`: UUID único del item
- `cart`: Referencia al carrito
- `product`: Producto del catálogo
- `quantity`: Cantidad del producto
- `created_at`: Fecha de creación
- `updated_at`: Fecha de última actualización

**Métodos:**
- `get_subtotal()`: Calcula el subtotal (precio × cantidad)
- `save()`: Valida el stock antes de guardar

## Operaciones CRUD

### CREATE (Crear)
**Vista:** `add_to_cart(request, product_id)`
- Agrega un producto al carrito
- Si el producto ya existe, incrementa la cantidad
- Valida stock disponible
- URL: `/cart/add/<product_id>/`

### READ (Leer)
**Vista:** `cart_view(request)`
- Muestra todos los items del carrito
- Calcula totales y subtotales
- URL: `/cart/`

### UPDATE (Actualizar)
**Vista:** `update_cart(request, product_id)`
- Actualiza la cantidad de un producto en el carrito
- Valida stock disponible
- Si cantidad es 0, elimina el item
- URL: `/cart/update/<product_id>/`

### DELETE (Eliminar)
**Vistas:**
1. `remove_from_cart(request, product_id)`
   - Elimina un producto específico del carrito
   - URL: `/cart/remove/<product_id>/`

2. `clear_cart(request)`
   - Elimina todos los productos del carrito
   - URL: `/cart/clear/`

## Características Adicionales

### Soporte para Usuarios Anónimos
- Los usuarios no autenticados pueden usar el carrito basado en sesiones
- Al iniciar sesión, su carrito se migra automáticamente a la base de datos

### Context Processor
- `cart_context`: Agrega `cart_count` a todas las plantillas
- Muestra el número de items en el carrito en el navbar

### Signals (Señales)
- `merge_cart_on_login`: Migra automáticamente el carrito de sesión cuando el usuario inicia sesión

### Utilidades (`utils.py`)
- `migrate_session_cart_to_db()`: Migra carrito de sesión a BD
- `validate_cart_stock()`: Valida stock de todos los items
- `clean_unavailable_products()`: Elimina productos no disponibles

### Admin
Panel de administración completo con:
- Vista de carritos con información del propietario
- Inline de items del carrito
- Filtros por fecha
- Búsqueda por usuario
- Cálculos de totales

## URLs Disponibles

```python
cart/                          # Ver carrito (READ)
cart/add/<product_id>/         # Agregar al carrito (CREATE)
cart/update/<product_id>/      # Actualizar cantidad (UPDATE)
cart/remove/<product_id>/      # Eliminar item (DELETE)
cart/clear/                    # Limpiar carrito (DELETE)
cart/checkout/                 # Proceso de checkout
cart/api/count/                # API: obtener conteo (JSON)
```

## API Endpoints

### GET /cart/api/count/
Retorna información del carrito en formato JSON:
```json
{
  "count": 5,
  "total": 125.50
}
```

## Tests
Suite completa de tests incluida en `tests.py`:
- Tests de modelos
- Tests de vistas CRUD
- Tests de validación de stock
- Tests de carritos anónimos y autenticados

**Ejecutar tests:**
```bash
python manage.py test app_cart
```

## Validaciones

### Stock
- Valida que la cantidad solicitada no exceda el stock disponible
- Actualiza automáticamente si el stock cambia
- Previene overselling

### Disponibilidad
- Verifica que el producto esté disponible antes de agregar
- Puede limpiar productos no disponibles automáticamente

### Unique Together
- Un carrito no puede tener el mismo producto duplicado
- La cantidad se actualiza en lugar de crear duplicados

## Migración
Se incluye migración `0001_initial.py` que crea:
- Tabla `app_cart_cart`
- Tabla `app_cart_cartitem`
- Relaciones con usuarios y productos
- Índices y constraints

## Integración con Otras Apps

### app_products
- Usa el modelo `Product` para los items del carrito
- Valida stock y disponibilidad

### app_login
- Asocia carritos con usuarios autenticados
- Usa `CustomUser` como modelo de usuario

### app_orders (futuro)
- El checkout creará órdenes desde el carrito
- Los items del carrito se transferirán a order items

## Uso Básico

### En las Vistas
```python
from app_cart.views import get_or_create_cart

def mi_vista(request):
    cart = get_or_create_cart(request)
    total = cart.get_total()
    items_count = cart.get_total_items()
    # ...
```

### En las Plantillas
```html
<!-- El cart_count está disponible en todas las plantillas -->
<span class="badge">{{ cart_count }}</span>

<!-- En la página del carrito -->
{% for item in cart_items %}
    <div>
        {{ item.product.name }} - 
        Cantidad: {{ item.quantity }} - 
        Subtotal: ${{ item.get_subtotal }}
    </div>
{% endfor %}

<div>Total: ${{ cart.get_total }}</div>
```

### Formularios
```html
<!-- Agregar al carrito -->
<form method="post" action="{% url 'cart:add_to_cart' product.id %}">
    {% csrf_token %}
    <input type="number" name="quantity" value="1" min="1">
    <button type="submit">Agregar al Carrito</button>
</form>

<!-- Actualizar cantidad -->
<form method="post" action="{% url 'cart:update_cart' item.product.id %}">
    {% csrf_token %}
    <input type="number" name="quantity" value="{{ item.quantity }}">
    <button type="submit">Actualizar</button>
</form>

<!-- Eliminar del carrito -->
<form method="post" action="{% url 'cart:remove_from_cart' item.product.id %}">
    {% csrf_token %}
    <button type="submit">Eliminar</button>
</form>
```

## Próximas Mejoras
- [ ] Cupones de descuento
- [ ] Guardado de carritos para más tarde
- [ ] Carritos compartidos
- [ ] Notificaciones de cambios de precio
- [ ] Recomendaciones basadas en el carrito
