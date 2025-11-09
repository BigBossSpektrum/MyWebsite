#!/bin/bash

# Script de Verificación - Gestión de Imágenes de Productos
# Ejecutar desde la raíz del proyecto

echo "================================================"
echo "   Verificación de Gestión de Imágenes"
echo "================================================"
echo ""

# Verificar que estamos en el directorio correcto
if [ ! -f "manage.py" ]; then
    echo "❌ Error: Este script debe ejecutarse desde la raíz del proyecto (donde está manage.py)"
    exit 1
fi

echo "✅ Directorio correcto detectado"
echo ""

# Verificar entorno virtual
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  Advertencia: No se detectó un entorno virtual activo"
    echo "   Recomendación: Activar el entorno virtual con: source env/bin/activate"
else
    echo "✅ Entorno virtual activo: $VIRTUAL_ENV"
fi
echo ""

# Verificar archivos modificados
echo "📁 Verificando archivos modificados..."
files=(
    "app_products/forms.py"
    "app_products/views.py"
    "app_products/templates/products/admin/product_form.html"
    "app_products/templates/products/admin/product_images.html"
    "static/css/products/admin_products.css"
)

all_exist=true
for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ❌ $file (no encontrado)"
        all_exist=false
    fi
done
echo ""

# Verificar documentación
echo "📄 Verificando documentación..."
docs=(
    "app_products/MEJORAS_GESTION_IMAGENES.md"
    "app_products/GUIA_RAPIDA_IMAGENES.md"
)

for doc in "${docs[@]}"; do
    if [ -f "$doc" ]; then
        echo "  ✅ $doc"
    else
        echo "  ❌ $doc (no encontrado)"
    fi
done
echo ""

# Verificar dependencias
echo "📦 Verificando dependencias..."
if command -v python3 &> /dev/null; then
    if python3 -c "import PIL" 2>/dev/null; then
        echo "  ✅ Pillow (PIL) instalado"
    else
        echo "  ❌ Pillow (PIL) no encontrado"
        echo "     Instalar con: pip install Pillow"
    fi
    
    if python3 -c "import django" 2>/dev/null; then
        echo "  ✅ Django instalado"
    else
        echo "  ❌ Django no encontrado"
    fi
else
    echo "  ❌ Python3 no encontrado"
fi
echo ""

# Verificar carpeta media
echo "📂 Verificando carpeta media..."
if [ -d "media" ]; then
    echo "  ✅ Carpeta 'media' existe"
    if [ -d "media/products" ]; then
        echo "  ✅ Subcarpeta 'media/products' existe"
    else
        echo "  ⚠️  Subcarpeta 'media/products' no existe (se creará automáticamente)"
    fi
else
    echo "  ⚠️  Carpeta 'media' no existe (se creará automáticamente)"
fi
echo ""

# Verificar migraciones
echo "🔄 Verificando migraciones..."
if [ -f "app_products/migrations/0001_initial.py" ]; then
    echo "  ✅ Migraciones iniciales existen"
    echo "  ℹ️  Recuerda ejecutar: python manage.py migrate"
else
    echo "  ❌ No se encontraron migraciones"
    echo "     Crear con: python manage.py makemigrations"
fi
echo ""

# Resumen
echo "================================================"
echo "   RESUMEN"
echo "================================================"

if $all_exist; then
    echo "✅ Todos los archivos principales están presentes"
else
    echo "⚠️  Algunos archivos no se encontraron"
fi

echo ""
echo "📋 Próximos pasos recomendados:"
echo "   1. Activar entorno virtual: source env/bin/activate"
echo "   2. Verificar dependencias: pip install -r requirements.txt"
echo "   3. Ejecutar migraciones: python manage.py migrate"
echo "   4. Crear superusuario (si no existe): python manage.py createsuperuser"
echo "   5. Ejecutar servidor: python manage.py runserver"
echo "   6. Acceder a: http://127.0.0.1:8000/admin/products/"
echo ""
echo "📖 Documentación:"
echo "   - Guía técnica: app_products/MEJORAS_GESTION_IMAGENES.md"
echo "   - Guía de usuario: app_products/GUIA_RAPIDA_IMAGENES.md"
echo ""
echo "================================================"
