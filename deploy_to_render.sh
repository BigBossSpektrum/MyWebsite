#!/bin/bash
# Script para desplegar a Render
# Ejecutar con: bash deploy_to_render.sh

echo "🚀 Preparando despliegue a Render..."
echo ""

# 1. Verificar configuración
echo "📋 Paso 1: Verificando configuración..."
python verify_render_config.py
if [ $? -ne 0 ]; then
    echo "❌ Verificación falló. Por favor revisa los errores."
    exit 1
fi
echo ""

# 2. Arreglar build.sh
echo "🔧 Paso 2: Verificando build.sh..."
python fix_build_script.py
echo ""

# 3. Mostrar cambios
echo "📝 Paso 3: Archivos modificados:"
git status --short
echo ""

# 4. Añadir archivos
echo "➕ Paso 4: Añadiendo archivos al commit..."
git add .
echo "✅ Archivos añadidos"
echo ""

# 5. Commit
echo "💾 Paso 5: Creando commit..."
read -p "¿Deseas continuar con el commit? (s/n): " confirm
if [ "$confirm" != "s" ] && [ "$confirm" != "S" ]; then
    echo "❌ Despliegue cancelado"
    exit 0
fi

git commit -m "Fix: Configuración para despliegue en Render

- Añadido comando setup_site para crear objeto Site
- Actualizado build.sh con setup automático
- Mejorado render.yaml con variables de entorno OAuth
- Añadida configuración de seguridad para producción
- Documentación completa de despliegue"

echo "✅ Commit creado"
echo ""

# 6. Push
echo "🚀 Paso 6: Enviando cambios a GitHub..."
read -p "¿Deseas hacer push a GitHub? (s/n): " confirm_push
if [ "$confirm_push" != "s" ] && [ "$confirm_push" != "S" ]; then
    echo "⚠️  Cambios commiteados pero NO enviados a GitHub"
    echo "   Puedes hacer push manualmente con: git push"
    exit 0
fi

git push origin Development---Check

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ ¡Despliegue iniciado!"
    echo ""
    echo "📋 Próximos pasos:"
    echo "1. Ve a https://dashboard.render.com"
    echo "2. El despliegue comenzará automáticamente"
    echo "3. Configura las variables de entorno OAuth en el Dashboard"
    echo "4. Espera a que el build complete (5-10 minutos)"
    echo "5. Visita: https://mywebsite-tlxs.onrender.com"
    echo ""
    echo "📖 Ver guía completa: DEPLOY_RENDER.md"
else
    echo "❌ Error al hacer push"
    exit 1
fi
