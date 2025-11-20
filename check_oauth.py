import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Zultech_main.settings')
django.setup()

from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site

print("=== Verificación de Configuración OAuth ===\n")

# Verificar Sites
print("1. Sites configurados:")
sites = Site.objects.all()
print(f"   Total: {sites.count()}")
for site in sites:
    print(f"   - ID: {site.id}, Domain: {site.domain}, Name: {site.name}")

print("\n2. Aplicaciones Sociales configuradas:")
apps = SocialApp.objects.all()
print(f"   Total: {apps.count()}")
for app in apps:
    print(f"   - Provider: {app.provider}")
    print(f"     Name: {app.name}")
    print(f"     Client ID: {app.client_id[:30]}...")
    print(f"     Sites: {', '.join([s.domain for s in app.sites.all()])}")
    print()

if apps.count() == 0:
    print("\n⚠️  NO HAY APLICACIONES SOCIALES CONFIGURADAS")
    print("\nPara configurar Google OAuth:")
    print("1. Ve a http://localhost:8000/admin/")
    print("2. Busca 'Social applications' en la sección SOCIAL ACCOUNTS")
    print("3. Haz clic en 'Add Social application'")
    print("4. Configura:")
    print("   - Provider: Google")
    print("   - Name: Google OAuth")
    print("   - Client id: tu-client-id.apps.googleusercontent.com")
    print("   - Secret key: tu-client-secret")
    print("   - Sites: selecciona localhost:8000 o el site correspondiente")
