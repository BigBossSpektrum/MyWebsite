#!/bin/bash
# INSTRUCCIONES URGENTES - Base de datos no configurada en Render

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  ⚠️  PROBLEMA CRÍTICO: SQLite en vez de PostgreSQL           ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "Tu aplicación en Render está usando SQLite (base de datos local)"
echo "en lugar de PostgreSQL. Esto causa el error 'no such table'."
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "  SOLUCIÓN RÁPIDA (5 minutos)"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "PASO 1: Ir a Render Dashboard"
echo "  → https://dashboard.render.com"
echo ""
echo "PASO 2: Verifica si tienes una base de datos PostgreSQL"
echo "  → En el menú lateral, busca 'PostgreSQL'"
echo "  → Si NO existe, créala:"
echo "     - Click 'New +' → PostgreSQL"
echo "     - Name: zultech-main-db"
echo "     - Region: Igual que tu web service"
echo "     - Plan: Free"
echo "     - Click 'Create Database'"
echo ""
echo "PASO 3: Conectar la base de datos a tu servicio web"
echo "  → Ve a tu web service (mywebsite-tlxs)"
echo "  → Click en 'Environment' (menú izquierdo)"
echo "  → Busca si existe 'DATABASE_URL'"
echo ""
echo "  Si NO existe DATABASE_URL:"
echo "     - Click 'Add Environment Variable'"
echo "     - Key: DATABASE_URL"
echo "     - Value: Copia de tu base de datos:"
echo "       1. Ve a tu base de datos PostgreSQL"
echo "       2. En 'Info', copia 'Internal Database URL'"
echo "       3. Pégala como valor de DATABASE_URL"
echo "     - Click 'Save Changes'"
echo ""
echo "  Si SÍ existe DATABASE_URL pero está vacío:"
echo "     - Click en el ícono de editar"
echo "     - Copia la Internal Database URL de tu BD"
echo "     - Pégala como valor"
echo "     - Click 'Save Changes'"
echo ""
echo "PASO 4: Forzar nuevo despliegue"
echo "  → En tu web service, ve a 'Manual Deploy'"
echo "  → Click 'Clear build cache & deploy'"
echo "  → Espera 5-10 minutos"
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "  VERIFICACIÓN"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "Cuando el build termine:"
echo "  1. Ve a 'Shell' en tu web service"
echo "  2. Ejecuta: python manage.py diagnose_db"
echo "  3. Debe decir: 'Using PostgreSQL (Production)'"
echo "  4. NO debe decir: 'Using SQLite'"
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo ""
read -p "¿Ya configuraste DATABASE_URL en Render? (s/n): " configured

if [ "$configured" = "s" ] || [ "$configured" = "S" ]; then
    echo ""
    echo "✅ Excelente! Ahora vamos a hacer commit y push de las mejoras:"
    echo ""
    
    # Show changes
    echo "Archivos modificados:"
    git status --short
    echo ""
    
    read -p "¿Hacer commit de estos cambios? (s/n): " do_commit
    if [ "$do_commit" = "s" ] || [ "$do_commit" = "S" ]; then
        git add .
        git commit -m "Fix: Forzar uso de PostgreSQL en Render

- Mejorada detección de DATABASE_URL
- Añadido comando diagnose_db para debugging
- Actualizado render.yaml con nombres correctos
- Añadido diagnóstico en build.sh
- Documentación de solución de problemas"
        
        echo ""
        read -p "¿Hacer push a GitHub? (s/n): " do_push
        if [ "$do_push" = "s" ] || [ "$do_push" = "S" ]; then
            git push origin Development---Check
            echo ""
            echo "✅ Cambios enviados! Render re-desplegará automáticamente."
            echo ""
            echo "Monitorea el progreso en:"
            echo "https://dashboard.render.com/web/mywebsite-tlxs/deploys"
        fi
    fi
else
    echo ""
    echo "⚠️  IMPORTANTE: Primero configura DATABASE_URL en Render"
    echo ""
    echo "Sin DATABASE_URL, la aplicación seguirá usando SQLite"
    echo "y el error persistirá."
    echo ""
    echo "Después de configurar, ejecuta este script de nuevo."
fi

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "📖 Documentación completa: FIX_DATABASE_RENDER.md"
echo "═══════════════════════════════════════════════════════════════"
