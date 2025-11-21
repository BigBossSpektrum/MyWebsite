"""
Script para limpiar sitios duplicados y configurar correctamente.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Zultech_main.settings')
django.setup()

from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp

def fix_sites():
    """Limpia sitios duplicados y configura correctamente."""
    
    # Eliminar todos los sitios excepto el primero
    sites = Site.objects.all().order_by('id')
    main_site = sites.first()
    
    print(f"Sitio principal: {main_site.domain} (ID: {main_site.id})")
    
    # Actualizar el sitio principal
    main_site.domain = '127.0.0.1:8000'
    main_site.name = 'Zultech'
    main_site.save()
    print(f"✓ Sitio principal actualizado a: {main_site.domain}")
    
    # Eliminar sitios duplicados
    duplicate_count = 0
    for site in sites[1:]:
        print(f"✗ Eliminando sitio duplicado: {site.domain} (ID: {site.id})")
        site.delete()
        duplicate_count += 1
    
    if duplicate_count > 0:
        print(f"✓ {duplicate_count} sitio(s) duplicado(s) eliminado(s)")
    else:
        print("✓ No hay sitios duplicados")
    
    # Reasociar todas las aplicaciones sociales con el sitio principal
    social_apps = SocialApp.objects.all()
    for app in social_apps:
        app.sites.clear()
        app.sites.add(main_site)
        print(f"✓ {app.provider} asociado con {main_site.domain}")
    
    print("\n¡Configuración completada!")
    print(f"Sitio configurado: {main_site.domain}")
    print(f"Aplicaciones sociales: {[app.provider for app in social_apps]}")

if __name__ == '__main__':
    fix_sites()
