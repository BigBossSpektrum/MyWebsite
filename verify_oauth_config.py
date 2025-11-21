import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Zultech_main.settings')
django.setup()

from django.conf import settings
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp

print("=== Verificación de Configuración OAuth ===\n")

# 1. Verificar variables de entorno
print("1. Variables de Entorno:")
google_id = os.environ.get('OAUTH_GOOGLE_ID')
google_secret = os.environ.get('OAUTH_GOOGLE_SECRET')

if google_id:
    print(f"   ✅ OAUTH_GOOGLE_ID: {google_id[:30]}...")
else:
    print("   ❌ OAUTH_GOOGLE_ID: NO CONFIGURADO")

if google_secret:
    print(f"   ✅ OAUTH_GOOGLE_SECRET: {'*' * 20}")
else:
    print("   ❌ OAUTH_GOOGLE_SECRET: NO CONFIGURADO")

# 2. Verificar SOCIALACCOUNT_PROVIDERS
print("\n2. Configuración en settings.py:")
if hasattr(settings, 'SOCIALACCOUNT_PROVIDERS'):
    providers = settings.SOCIALACCOUNT_PROVIDERS
    print(f"   ✅ SOCIALACCOUNT_PROVIDERS configurado")
    
    if 'google' in providers:
        print("   ✅ Provider 'google' encontrado")
        google_config = providers['google']
        
        if 'APP' in google_config:
            app_config = google_config['APP']
            print(f"   ✅ Client ID: {app_config.get('client_id', 'NO CONFIGURADO')[:30]}...")
            print(f"   ✅ Secret: {'Configurado' if app_config.get('secret') else 'NO CONFIGURADO'}")
        else:
            print("   ❌ Falta configuración 'APP'")
    else:
        print("   ❌ Provider 'google' no encontrado")
else:
    print("   ❌ SOCIALACCOUNT_PROVIDERS no configurado")

# 3. Verificar Sites
print("\n3. Sites Configurados:")
sites = Site.objects.all()
print(f"   Total: {sites.count()}")
for site in sites:
    marker = "✅" if site.id == settings.SITE_ID else "  "
    print(f"   {marker} ID: {site.id}, Domain: {site.domain}, Name: {site.name}")

# 4. Verificar Social Apps en Admin
print("\n4. Social Apps en Admin:")
apps = SocialApp.objects.all()
if apps.exists():
    print(f"   ⚠️  Hay {apps.count()} app(s) en el admin (puede causar conflictos)")
    for app in apps:
        print(f"      - {app.provider}: {app.name}")
else:
    print("   ✅ Sin apps en admin (usando configuración de settings.py)")

# 5. Verificar SOCIALACCOUNT_ADAPTER
print("\n5. Adapter Personalizado:")
if hasattr(settings, 'SOCIALACCOUNT_ADAPTER'):
    print(f"   ✅ {settings.SOCIALACCOUNT_ADAPTER}")
else:
    print("   ⚠️  No configurado (usará el adapter por defecto)")

# 6. Resumen
print("\n" + "="*50)
print("RESUMEN:")
print("="*50)

all_ok = True

if not google_id or not google_secret:
    print("❌ Variables de entorno faltantes")
    all_ok = False
else:
    print("✅ Variables de entorno configuradas")

if hasattr(settings, 'SOCIALACCOUNT_PROVIDERS') and 'google' in settings.SOCIALACCOUNT_PROVIDERS:
    print("✅ SOCIALACCOUNT_PROVIDERS configurado correctamente")
else:
    print("❌ SOCIALACCOUNT_PROVIDERS no configurado")
    all_ok = False

if not apps.exists():
    print("✅ Sin conflictos en admin")
else:
    print("⚠️  Hay apps en admin que pueden causar conflictos")

if all_ok and not apps.exists():
    print("\n🎉 ¡Configuración lista! Puedes probar el login con Google")
    print(f"   URL: http://localhost:8000/accounts/login/")
else:
    print("\n⚠️  Hay problemas que deben corregirse")
