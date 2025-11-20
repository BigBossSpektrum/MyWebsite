import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Zultech_main.settings')
django.setup()

from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site

print("=== Diagnóstico Completo ===\n")

# 1. Verificar Sites
print("1. SITES:")
sites = Site.objects.all()
for site in sites:
    print(f"   - ID: {site.id}, Domain: {site.domain}, Name: {site.name}")

# 2. Verificar Social Apps
print("\n2. SOCIAL APPS:")
apps = SocialApp.objects.all()
for app in apps:
    print(f"   - Provider: {app.provider}, Name: {app.name}, ID: {app.id}")
    print(f"     Sites asociados: {[s.domain for s in app.sites.all()]}")

# 3. Verificar SITE_ID en settings
from django.conf import settings
print(f"\n3. SITE_ID en settings: {settings.SITE_ID}")

# 4. Verificar si el SITE_ID existe
try:
    current_site = Site.objects.get(id=settings.SITE_ID)
    print(f"   Site actual: {current_site.domain}")
except Site.DoesNotExist:
    print(f"   ⚠️ WARNING: Site con ID {settings.SITE_ID} no existe")

# 5. Verificar cuántas Google apps tienen el site actual
print("\n4. DIAGNÓSTICO DEL PROBLEMA:")
google_apps = SocialApp.objects.filter(provider='google')
print(f"   Total Google apps: {google_apps.count()}")

for app in google_apps:
    app_sites = app.sites.all()
    print(f"\n   App '{app.name}' (ID: {app.id}):")
    print(f"   - Sites count: {app_sites.count()}")
    print(f"   - Sites: {[f'{s.id}:{s.domain}' for s in app_sites]}")
    
    # Verificar si tiene el site actual
    has_current_site = app.sites.filter(id=settings.SITE_ID).exists()
    print(f"   - Tiene site ID {settings.SITE_ID}: {has_current_site}")

# 6. Solución propuesta
print("\n5. SOLUCIÓN:")
print("   El problema puede ser que la app está asociada a múltiples sites")
print("   o que hay problemas con la relación ManyToMany.")

if google_apps.count() == 1:
    app = google_apps.first()
    current_site = Site.objects.get(id=settings.SITE_ID)
    
    print(f"\n   Reconfigurar '{app.name}' para usar solo '{current_site.domain}'?")
    print("   Esto eliminará asociaciones con otros sites.")
    
    choice = input("\n   ¿Proceder? (s/n): ").strip().lower()
    
    if choice == 's':
        app.sites.clear()
        app.sites.add(current_site)
        print(f"\n   ✅ '{app.name}' ahora está asociado solo a '{current_site.domain}'")
    else:
        print("\n   Operación cancelada.")
