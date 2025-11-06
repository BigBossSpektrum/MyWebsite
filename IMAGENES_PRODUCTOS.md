# Configuración de Imágenes de Productos

## Configuración Actual

La configuración de media files está correctamente establecida:

- **MEDIA_URL**: `/media/`
- **MEDIA_ROOT**: `BASE_DIR / 'media'`
- **Upload path**: `products/` (dentro de media)

## Cómo Añadir Productos con Imágenes

### Opción 1: A través del Admin de Django

1. Accede al panel de administración: `http://127.0.0.1:8000/admin/`
2. Ve a la sección "Products"
3. Haz clic en "Add Product" o "Añadir Producto"
4. Completa los campos del producto:
   - Nombre
   - Slug (se genera automáticamente)
   - Categoría
   - Descripción
   - Precio
   - Stock
   - Disponible (checkbox)
5. En la sección de imágenes inline, haz clic en "Add another Product Image"
6. Sube la imagen
7. Marca "Is main" para la imagen principal
8. Guarda el producto

### Opción 2: Directamente crear ProductImage

1. Ve a "Product images" en el admin
2. Haz clic en "Add Product Image"
3. Selecciona el producto
4. Sube la imagen
5. Añade texto alternativo (opcional)
6. Marca "Is main" si es la imagen principal
7. Guarda

## Estructura de Archivos

```
media/
└── products/
    ├── imagen1.jpg
    ├── imagen2.png
    └── ...
```

## Imagen Placeholder

Si un producto no tiene imagen, se mostrará automáticamente un placeholder SVG ubicado en:
`static/img/products/no-image.svg`

## Verificar Configuración

Para verificar que las imágenes se están sirviendo correctamente:

1. Asegúrate de que el servidor esté corriendo: `python manage.py runserver`
2. Sube una imagen a través del admin
3. Verifica que la imagen aparezca en la lista de productos: `http://127.0.0.1:8000/products/`

## Troubleshooting

Si las imágenes no cargan:

1. Verifica que `DEBUG = True` en settings.py
2. Verifica que la carpeta `media/products/` exista
3. Verifica los permisos de la carpeta media
4. Revisa la consola del navegador para errores 404
5. Asegúrate de que la URL de la imagen sea correcta (debe empezar con `/media/products/`)

## Formatos de Imagen Recomendados

- JPG/JPEG: Para fotografías de productos
- PNG: Para imágenes con transparencia
- WebP: Para mejor compresión (navegadores modernos)

Tamaño recomendado: 800x600 px o mayor para buena calidad.
