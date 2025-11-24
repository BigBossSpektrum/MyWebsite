@echo off
REM Script para desplegar a Render (Windows)
REM Ejecutar con: deploy_to_render.bat

echo.
echo ========================================
echo   Preparando despliegue a Render
echo ========================================
echo.

REM 1. Verificar configuracion
echo [1/6] Verificando configuracion...
python verify_render_config.py
if errorlevel 1 (
    echo.
    echo ERROR: Verificacion fallo. Por favor revisa los errores.
    pause
    exit /b 1
)
echo.

REM 2. Arreglar build.sh
echo [2/6] Verificando build.sh...
python fix_build_script.py
echo.

REM 3. Mostrar cambios
echo [3/6] Archivos modificados:
git status --short
echo.

REM 4. Anadir archivos
echo [4/6] Anadiendo archivos al commit...
git add .
echo OK - Archivos anadidos
echo.

REM 5. Commit
echo [5/6] Creando commit...
set /p confirm="Deseas continuar con el commit? (s/n): "
if /i not "%confirm%"=="s" (
    echo.
    echo CANCELADO: Despliegue cancelado
    pause
    exit /b 0
)

git commit -m "Fix: Configuracion para despliegue en Render - Anadido comando setup_site para crear objeto Site - Actualizado build.sh con setup automatico - Mejorado render.yaml con variables de entorno OAuth - Anadida configuracion de seguridad para produccion - Documentacion completa de despliegue"

echo OK - Commit creado
echo.

REM 6. Push
echo [6/6] Enviando cambios a GitHub...
set /p confirm_push="Deseas hacer push a GitHub? (s/n): "
if /i not "%confirm_push%"=="s" (
    echo.
    echo NOTA: Cambios commiteados pero NO enviados a GitHub
    echo       Puedes hacer push manualmente con: git push
    pause
    exit /b 0
)

git push origin Development---Check

if errorlevel 1 (
    echo.
    echo ERROR: Error al hacer push
    pause
    exit /b 1
)

echo.
echo ========================================
echo   Despliegue iniciado exitosamente!
echo ========================================
echo.
echo Proximos pasos:
echo 1. Ve a https://dashboard.render.com
echo 2. El despliegue comenzara automaticamente
echo 3. Configura las variables de entorno OAuth en el Dashboard
echo 4. Espera a que el build complete (5-10 minutos)
echo 5. Visita: https://mywebsite-tlxs.onrender.com
echo.
echo Ver guia completa: DEPLOY_RENDER.md
echo.
pause
