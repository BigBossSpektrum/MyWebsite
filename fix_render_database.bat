@echo off
setlocal enabledelayedexpansion

echo.
echo ================================================================
echo   PROBLEMA CRITICO: SQLite en vez de PostgreSQL
echo ================================================================
echo.
echo Tu aplicacion en Render esta usando SQLite (base de datos local)
echo en lugar de PostgreSQL. Esto causa el error 'no such table'.
echo.
echo ================================================================
echo   SOLUCION RAPIDA (5 minutos)
echo ================================================================
echo.
echo PASO 1: Ir a Render Dashboard
echo   ^> https://dashboard.render.com
echo.
echo PASO 2: Verifica si tienes una base de datos PostgreSQL
echo   ^> En el menu lateral, busca 'PostgreSQL'
echo   ^> Si NO existe, creala:
echo      - Click 'New +' -^> PostgreSQL
echo      - Name: zultech-main-db
echo      - Region: Igual que tu web service
echo      - Plan: Free
echo      - Click 'Create Database'
echo.
echo PASO 3: Conectar la base de datos a tu servicio web
echo   ^> Ve a tu web service (mywebsite-tlxs)
echo   ^> Click en 'Environment' (menu izquierdo)
echo   ^> Busca si existe 'DATABASE_URL'
echo.
echo   Si NO existe DATABASE_URL:
echo      - Click 'Add Environment Variable'
echo      - Key: DATABASE_URL
echo      - Value: Copia de tu base de datos:
echo        1. Ve a tu base de datos PostgreSQL
echo        2. En 'Info', copia 'Internal Database URL'
echo        3. Pegala como valor de DATABASE_URL
echo      - Click 'Save Changes'
echo.
echo   Si SI existe DATABASE_URL pero esta vacio:
echo      - Click en el icono de editar
echo      - Copia la Internal Database URL de tu BD
echo      - Pegala como valor
echo      - Click 'Save Changes'
echo.
echo PASO 4: Forzar nuevo despliegue
echo   ^> En tu web service, ve a 'Manual Deploy'
echo   ^> Click 'Clear build cache ^& deploy'
echo   ^> Espera 5-10 minutos
echo.
echo ================================================================
echo   VERIFICACION
echo ================================================================
echo.
echo Cuando el build termine:
echo   1. Ve a 'Shell' en tu web service
echo   2. Ejecuta: python manage.py diagnose_db
echo   3. Debe decir: 'Using PostgreSQL (Production)'
echo   4. NO debe decir: 'Using SQLite'
echo.
echo ================================================================
echo.
set /p configured="Ya configuraste DATABASE_URL en Render? (s/n): "

if /i "%configured%"=="s" (
    echo.
    echo OK! Ahora vamos a hacer commit y push de las mejoras:
    echo.
    
    echo Archivos modificados:
    git status --short
    echo.
    
    set /p do_commit="Hacer commit de estos cambios? (s/n): "
    if /i "!do_commit!"=="s" (
        git add .
        git commit -m "Fix: Forzar uso de PostgreSQL en Render - Mejorada deteccion de DATABASE_URL - Anadido comando diagnose_db para debugging - Actualizado render.yaml con nombres correctos - Anadido diagnostico en build.sh - Documentacion de solucion de problemas"
        
        echo.
        set /p do_push="Hacer push a GitHub? (s/n): "
        if /i "!do_push!"=="s" (
            git push origin Development---Check
            echo.
            echo OK - Cambios enviados! Render re-desplegara automaticamente.
            echo.
            echo Monitorea el progreso en:
            echo https://dashboard.render.com/web/mywebsite-tlxs/deploys
        )
    )
) else (
    echo.
    echo IMPORTANTE: Primero configura DATABASE_URL en Render
    echo.
    echo Sin DATABASE_URL, la aplicacion seguira usando SQLite
    echo y el error persistira.
    echo.
    echo Despues de configurar, ejecuta este script de nuevo.
)

echo.
echo ================================================================
echo Documentacion completa: FIX_DATABASE_RENDER.md
echo ================================================================
echo.
pause
