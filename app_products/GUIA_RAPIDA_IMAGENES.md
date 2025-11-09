# Guía Rápida: Gestión de Imágenes de Productos

## 🚀 Inicio Rápido

### Crear Producto con Imágenes

1. **Accede al panel de administración**
   - URL: `/admin/products/`
   - Click en "Nuevo Producto" (botón azul superior derecho)

2. **Completa la información del producto**
   - Nombre
   - Slug (se genera automáticamente)
   - Descripción
   - Categoría
   - Precio
   - Stock
   - Disponibilidad

3. **Agrega imágenes**
   
   **Opción 1: Drag & Drop**
   - Arrastra las imágenes desde tu explorador de archivos
   - Suéltalas sobre la zona azul con el icono de nube
   
   **Opción 2: Selección Manual**
   - Click en la zona azul o en "Seleccionar Imágenes"
   - Selecciona una o múltiples imágenes
   - Click en "Abrir"

4. **Revisa las imágenes**
   - Verás una vista previa de cada imagen seleccionada
   - Puedes eliminar imágenes haciendo click en la "X" roja
   - La primera imagen será la imagen principal automáticamente

5. **Guarda el producto**
   - Click en "Crear"
   - Las imágenes se subirán junto con el producto

---

## 📝 Editar Producto y Agregar Más Imágenes

### Método 1: Desde el Formulario de Edición

1. En la lista de productos, click en el botón azul de edición (icono lápiz)
2. Modifica la información del producto si es necesario
3. Agrega nuevas imágenes usando drag & drop o selección manual
4. Las imágenes existentes se mantienen y se agregan las nuevas
5. Click en "Actualizar"

### Método 2: Gestor de Imágenes (Recomendado)

1. En la lista de productos, click en el botón amarillo de imágenes (icono de imágenes)
2. Verás todas las imágenes actuales del producto
3. Usa la zona de drag & drop superior para agregar nuevas imágenes
4. Gestiona cada imagen individualmente (ver siguiente sección)

---

## 🖼️ Gestionar Imágenes Existentes

### Ver Imágenes

- Accede desde la lista de productos (botón amarillo con icono de imágenes)
- Verás una galería con todas las imágenes del producto
- La imagen principal tiene un badge verde con estrella

### Editar Texto Alternativo

1. En cada tarjeta de imagen, encuentra el campo "Texto Alternativo"
2. Escribe una descripción de la imagen (para accesibilidad y SEO)
3. Click en "Guardar Cambios"

### Cambiar Imagen Principal

1. Marca el checkbox "Imagen Principal" en la imagen deseada
2. Click en "Guardar Cambios"
3. La imagen anterior dejará de ser principal automáticamente
4. Solo puede haber una imagen principal por producto

### Eliminar Imagen

1. Click en el botón rojo "Eliminar" en la tarjeta de imagen
2. Aparecerá un modal de confirmación con vista previa
3. Confirma la eliminación
4. La imagen se eliminará permanentemente

---

## ✅ Consejos y Mejores Prácticas

### Tamaño de Imágenes
- **Recomendado**: 1200x1200px o mayor para mejor calidad
- **Máximo**: 5MB por imagen
- **Formato**: JPG para fotografías, PNG para imágenes con transparencia

### Cantidad de Imágenes
- **Mínimo recomendado**: 3-5 imágenes por producto
- **Incluye**: Vista frontal, lateral, posterior, detalles, uso

### Texto Alternativo
- Describe lo que se ve en la imagen
- Útil para accesibilidad (lectores de pantalla)
- Mejora el SEO
- Ejemplo: "Laptop Dell XPS 13 vista frontal con pantalla encendida"

### Imagen Principal
- Debe ser la mejor imagen del producto
- Preferiblemente vista frontal o más representativa
- Se muestra en listados y como primera imagen en detalles

### Nombres de Archivo
- Usa nombres descriptivos antes de subir
- Evita caracteres especiales
- Ejemplo: `laptop-dell-xps-13-frontal.jpg`

---

## 🎨 Características de la Interfaz

### Drag & Drop
- **Zona activa**: Toda el área azul con icono de nube
- **Feedback visual**: El área cambia de color al arrastrar
- **Múltiples archivos**: Puedes arrastrar varios a la vez

### Vista Previa
- **Instantánea**: Se muestra apenas seleccionas las imágenes
- **Eliminar**: Click en la "X" roja para quitar de la selección
- **Reorganizar**: Las imágenes mantienen el orden de selección

### Validaciones
- **Tipo de archivo**: Solo acepta imágenes (JPG, PNG, GIF, WebP)
- **Tamaño**: Máximo 5MB por imagen
- **Alertas**: Recibirás notificaciones si hay errores

### Responsive
- **Desktop**: Vista completa con todas las características
- **Tablet**: Diseño adaptado con 3 columnas en galería
- **Mobile**: Vista optimizada con 2 columnas

---

## 🐛 Solución de Problemas

### "El archivo no es una imagen válida"
- Verifica que el archivo sea JPG, PNG, GIF o WebP
- Algunos archivos corruptos pueden causar este error

### "El archivo excede el tamaño máximo"
- Reduce el tamaño de la imagen antes de subirla
- Usa herramientas como TinyPNG o Squoosh
- Considera cambiar de PNG a JPG para menor tamaño

### "No se suben las imágenes"
- Verifica tu conexión a internet
- Asegúrate de hacer click en "Subir" o "Guardar"
- Revisa que el servidor tenga espacio disponible

### "La imagen no se ve"
- Verifica la configuración de MEDIA_ROOT en Django
- Asegúrate de que el servidor sirva archivos media
- Revisa permisos de carpetas en el servidor

---

## 📱 Atajos de Teclado

- **Ctrl/Cmd + Click**: Seleccionar múltiples archivos
- **Escape**: Cerrar modales
- **Enter**: Confirmar acciones en modales (cuando está enfocado)

---

## 🔒 Seguridad

- Solo administradores pueden gestionar imágenes
- Todas las acciones requieren autenticación
- Protección CSRF en todos los formularios
- Validación de tipos de archivo en servidor

---

## 📊 Límites del Sistema

- **Tamaño máximo por imagen**: 5MB
- **Formatos soportados**: JPG, JPEG, PNG, GIF, WebP
- **Imágenes por producto**: Ilimitado (recomendado 3-10)
- **Resolución recomendada**: 1200x1200px o superior

---

## 🆘 Soporte

Si encuentras problemas:
1. Verifica esta guía
2. Revisa la documentación técnica (MEJORAS_GESTION_IMAGENES.md)
3. Contacta al administrador del sistema
4. Reporta bugs con capturas de pantalla

---

## 🎯 Checklist de Verificación

Al agregar imágenes a un producto, verifica:

- [ ] Al menos 3 imágenes subidas
- [ ] Una imagen marcada como principal
- [ ] Texto alternativo en todas las imágenes
- [ ] Imágenes de buena calidad (mínimo 800x800px)
- [ ] Nombres de archivo descriptivos
- [ ] Imágenes muestran el producto desde diferentes ángulos
- [ ] Imágenes con buena iluminación y enfoque
- [ ] Formato apropiado (JPG para fotos, PNG para transparencias)

---

**Última actualización**: Noviembre 2025
**Versión del sistema**: 1.0
