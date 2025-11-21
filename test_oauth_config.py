"""
Script para probar la configuración de OAuth y detectar problemas.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Zultech_main.settings')
django.setup()

from django.conf import settings
from allauth.socialaccount.models import SocialApp
import json

print("\n" + "="*60)
print("DIAGNÓSTICO DE CONFIGURACIÓN OAUTH")
print("="*60)

# 1. Verificar configuración en settings
print("\n1. CONFIGURACIÓN EN SETTINGS.PY:")
print("-"*60)
providers = settings.SOCIALACCOUNT_PROVIDERS
print(json.dumps(providers, indent=2, default=str))

# 2. Verificar si hay SocialApp en la base de datos
print("\n2. SOCIALAPP EN BASE DE DATOS:")
print("-"*60)
social_apps = SocialApp.objects.all()
if social_apps.exists():
    print(f"⚠️  Encontrados {social_apps.count()} SocialApp en la base de datos:")
    for app in social_apps:
        print(f"  - {app.provider}: {app.name}")
    print("\n⚠️  PROBLEMA DETECTADO:")
    print("   Con configuración interna, allauth puede estar confundiéndose")
    print("   entre la configuración de settings.py y la base de datos.")
    print("\n   SOLUCIÓN: Ejecuta python clean_old_oauth_config.py")
else:
    print("✓ No hay SocialApp en la base de datos (correcto)")

# 3. Verificar que las credenciales estén completas
print("\n3. CREDENCIALES:")
print("-"*60)
for provider, config in providers.items():
    if 'APP' in config:
        app = config['APP']
        client_id = app.get('client_id', '')
        secret = app.get('secret', '')
        
        print(f"\n{provider.upper()}:")
        if client_id and secret:
            print(f"  ✓ Client ID: {client_id[:20]}...")
            print(f"  ✓ Secret: {'*' * 20}...")
        else:
            print(f"  ❌ PROBLEMA: Credenciales incompletas")
            if not client_id:
                print(f"     Falta: OAUTH_{provider.upper()}_ID")
            if not secret:
                print(f"     Falta: OAUTH_{provider.upper()}_SECRET")

# 4. Verificar SITE_ID
print("\n4. SITE_ID:")
print("-"*60)
if hasattr(settings, 'SITE_ID'):
    print(f"⚠️  SITE_ID = {settings.SITE_ID}")
    print("   Con configuración interna, esto puede causar conflictos")
else:
    print("✓ SITE_ID no está configurado (correcto)")

# 5. Verificar django.contrib.sites
print("\n5. DJANGO.CONTRIB.SITES:")
print("-"*60)
if 'django.contrib.sites' in settings.INSTALLED_APPS:
    print("⚠️  django.contrib.sites está en INSTALLED_APPS")
    print("   Esto puede causar que allauth busque en la base de datos")
else:
    print("✓ django.contrib.sites no está en INSTALLED_APPS")

print("\n" + "="*60)
print("DIAGNÓSTICO COMPLETADO")
print("="*60 + "\n")
