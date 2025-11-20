import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Zultech_main.settings')
django.setup()

from allauth.socialaccount.models import SocialApp

print("=== Limpieza de Social Apps del Admin ===\n")

# Obtener todas las aplicaciones sociales
apps = SocialApp.objects.all()

print(f"Aplicaciones encontradas: {apps.count()}\n")

for app in apps:
    print(f"- Provider: {app.provider}")
    print(f"  Name: {app.name}")
    print(f"  ID: {app.id}")
    print(f"  Sites: {[s.domain for s in app.sites.all()]}")

if apps.exists():
    print("\n⚠️  Estas aplicaciones serán eliminadas del admin.")
    print("La configuración ahora se manejará desde settings.py (SOCIALACCOUNT_PROVIDERS)")
    
    choice = input("\n¿Confirmar eliminación? (s/n): ").strip().lower()
    
    if choice == 's':
        count = apps.count()
        apps.delete()
        print(f"\n✅ {count} aplicación(es) eliminada(s) exitosamente")
        print("\nAhora las credenciales OAuth se cargan desde:")
        print("- Archivo: .env")
        print("- Configuración: settings.py (SOCIALACCOUNT_PROVIDERS)")
    else:
        print("\n❌ Operación cancelada")
else:
    print("\n✅ No hay aplicaciones sociales en el admin")
    print("Las credenciales se cargan desde settings.py")
