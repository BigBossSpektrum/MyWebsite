#!/usr/bin/env python
"""
Script para verificar la configuración de Cloudinary
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Zultech_main.settings')
django.setup()

from django.conf import settings

def check_cloudinary():
    print("="*60)
    print("🔍 VERIFICACIÓN DE CONFIGURACIÓN DE CLOUDINARY")
    print("="*60)
    
    # Verificar si está en Render
    is_render = settings.IS_RENDER
    print(f"\n📍 Entorno: {'Render (Producción)' if is_render else 'Local (Desarrollo)'}")
    
    # Verificar variables de entorno
    print("\n🔑 Variables de Entorno:")
    cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME', '')
    api_key = os.environ.get('CLOUDINARY_API_KEY', '')
    api_secret = os.environ.get('CLOUDINARY_API_SECRET', '')
    
    if cloud_name:
        print(f"   ✅ CLOUDINARY_CLOUD_NAME: {cloud_name}")
    else:
        print(f"   ❌ CLOUDINARY_CLOUD_NAME: No configurado")
    
    if api_key:
        print(f"   ✅ CLOUDINARY_API_KEY: {api_key[:8]}...")
    else:
        print(f"   ❌ CLOUDINARY_API_KEY: No configurado")
    
    if api_secret:
        print(f"   ✅ CLOUDINARY_API_SECRET: {api_secret[:8]}...")
    else:
        print(f"   ❌ CLOUDINARY_API_SECRET: No configurado")
    
    # Verificar configuración de Django
    print("\n⚙️ Configuración de Django:")
    
    if hasattr(settings, 'CLOUDINARY_STORAGE'):
        config = settings.CLOUDINARY_STORAGE
        print(f"   ✅ CLOUDINARY_STORAGE configurado")
        print(f"      Cloud Name: {config.get('CLOUD_NAME', 'No configurado')}")
    else:
        print(f"   ❌ CLOUDINARY_STORAGE no configurado")
    
    print(f"\n📁 MEDIA_URL: {settings.MEDIA_URL}")
    
    if hasattr(settings, 'DEFAULT_FILE_STORAGE'):
        storage = settings.DEFAULT_FILE_STORAGE
        print(f"📦 DEFAULT_FILE_STORAGE: {storage}")
        
        if 'cloudinary' in storage.lower():
            print("   ✅ Usando Cloudinary para almacenamiento")
        else:
            print("   ⚠️  Usando almacenamiento local")
    else:
        print("📦 DEFAULT_FILE_STORAGE: No configurado (usando default)")
    
    if settings.MEDIA_ROOT:
        print(f"📂 MEDIA_ROOT: {settings.MEDIA_ROOT}")
    else:
        print(f"📂 MEDIA_ROOT: None (usando Cloudinary)")
    
    # Verificar si Cloudinary está instalado
    print("\n📚 Paquetes Instalados:")
    try:
        import cloudinary
        print(f"   ✅ cloudinary: v{cloudinary.__version__}")
    except ImportError:
        print(f"   ❌ cloudinary: No instalado")
        print(f"      Ejecuta: pip install cloudinary")
    
    try:
        import cloudinary_storage
        print(f"   ✅ django-cloudinary-storage instalado")
    except ImportError:
        print(f"   ❌ django-cloudinary-storage: No instalado")
        print(f"      Ejecuta: pip install django-cloudinary-storage")
    
    # Probar conexión a Cloudinary
    if cloud_name and api_key and api_secret:
        print("\n🧪 Probando conexión a Cloudinary...")
        try:
            import cloudinary
            cloudinary.config(
                cloud_name=cloud_name,
                api_key=api_key,
                api_secret=api_secret
            )
            
            # Intentar hacer ping
            from cloudinary import api
            result = api.ping()
            
            if result.get('status') == 'ok':
                print("   ✅ Conexión exitosa a Cloudinary")
            else:
                print(f"   ⚠️  Respuesta inesperada: {result}")
        except Exception as e:
            print(f"   ❌ Error al conectar con Cloudinary: {e}")
    else:
        print("\n⚠️  No se puede probar conexión: faltan credenciales")
    
    # Recomendaciones
    print("\n" + "="*60)
    print("📋 RECOMENDACIONES")
    print("="*60)
    
    if not cloud_name or not api_key or not api_secret:
        print("\n❌ ACCIÓN REQUERIDA:")
        print("   1. Crea una cuenta en https://cloudinary.com")
        print("   2. Obtén tus credenciales del Dashboard")
        print("   3. Configura las variables de entorno:")
        print("      - CLOUDINARY_CLOUD_NAME")
        print("      - CLOUDINARY_API_KEY")
        print("      - CLOUDINARY_API_SECRET")
        if is_render:
            print("   4. Configúralas en Render Dashboard → Environment")
    else:
        print("\n✅ Configuración completa")
        print("   Las imágenes se guardarán en Cloudinary")
    
    print("\n" + "="*60)

if __name__ == '__main__':
    check_cloudinary()
