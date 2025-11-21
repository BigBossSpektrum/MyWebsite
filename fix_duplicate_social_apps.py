import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Zultech_main.settings')
django.setup()

from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site

print("=== Verificación de Aplicaciones Sociales ===\n")

# Verificar aplicaciones sociales de Google
google_apps = SocialApp.objects.filter(provider='google')
print(f"Aplicaciones de Google encontradas: {google_apps.count()}")

for i, app in enumerate(google_apps, 1):
    print(f"\n{i}. Google App ID: {app.id}")
    print(f"   Name: {app.name}")
    print(f"   Client ID: {app.client_id[:30]}...")
    print(f"   Sites: {', '.join([s.domain for s in app.sites.all()])}")

if google_apps.count() > 1:
    print("\n⚠️  PROBLEMA: Hay múltiples aplicaciones de Google configuradas")
    print("\nOpciones:")
    print("1. Mantener solo la primera y eliminar duplicadas")
    print("2. Mantener la última y eliminar anteriores")
    print("3. Ver más detalles")
    
    choice = input("\nElige una opción (1-3): ").strip()
    
    if choice == "1":
        # Mantener la primera, eliminar el resto
        keep_app = google_apps.first()
        delete_apps = google_apps.exclude(id=keep_app.id)
        print(f"\nManteniendo: {keep_app.name} (ID: {keep_app.id})")
        print(f"Eliminando {delete_apps.count()} aplicación(es)...")
        delete_apps.delete()
        print("✅ Duplicados eliminados exitosamente")
        
    elif choice == "2":
        # Mantener la última, eliminar el resto
        keep_app = google_apps.last()
        delete_apps = google_apps.exclude(id=keep_app.id)
        print(f"\nManteniendo: {keep_app.name} (ID: {keep_app.id})")
        print(f"Eliminando {delete_apps.count()} aplicación(es)...")
        delete_apps.delete()
        print("✅ Duplicados eliminados exitosamente")
        
    elif choice == "3":
        # Mostrar más detalles
        for app in google_apps:
            print(f"\n{'='*50}")
            print(f"ID: {app.id}")
            print(f"Name: {app.name}")
            print(f"Provider: {app.provider}")
            print(f"Client ID: {app.client_id}")
            print(f"Secret: {'*' * 20}")
            print(f"Sites: {[s.domain for s in app.sites.all()]}")
        
        print("\n⚠️  Por favor, elimina manualmente los duplicados en el admin:")
        print("http://localhost:8000/admin/socialaccount/socialapp/")
else:
    print("\n✅ No hay duplicados. La configuración está correcta.")

print("\n=== Resumen Final ===")
google_apps = SocialApp.objects.filter(provider='google')
print(f"Aplicaciones de Google: {google_apps.count()}")
