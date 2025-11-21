"""
Script para configurar las aplicaciones sociales en la base de datos.
Ejecutar con: python setup_social_apps.py
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Zultech_main.settings')
django.setup()

from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def setup_social_apps():
    """Configura las aplicaciones sociales en la base de datos."""
    
    # Obtener el site actual
    site = Site.objects.get_current()
    print(f"Configurando para el sitio: {site.domain}")
    
    # Configurar Google OAuth
    google_client_id = os.getenv('OAUTH_GOOGLE_ID')
    google_secret = os.getenv('OAUTH_GOOGLE_SECRET')
    
    if google_client_id and google_secret:
        google_app, created = SocialApp.objects.get_or_create(
            provider='google',
            defaults={
                'name': 'Google OAuth',
                'client_id': google_client_id,
                'secret': google_secret,
            }
        )
        
        if not created:
            # Actualizar si ya existe
            google_app.client_id = google_client_id
            google_app.secret = google_secret
            google_app.save()
            print("✓ Google OAuth actualizado")
        else:
            print("✓ Google OAuth creado")
        
        # Asociar con el sitio actual
        if site not in google_app.sites.all():
            google_app.sites.add(site)
            print(f"  - Asociado con el sitio {site.domain}")
    else:
        print("✗ Google OAuth: Faltan credenciales en .env (OAUTH_GOOGLE_ID, OAUTH_GOOGLE_SECRET)")
    
    # Configurar GitHub OAuth
    github_client_id = os.getenv('OAUTH_GITHUB_ID')
    github_secret = os.getenv('OAUTH_GITHUB_SECRET')
    
    if github_client_id and github_secret:
        github_app, created = SocialApp.objects.get_or_create(
            provider='github',
            defaults={
                'name': 'GitHub OAuth',
                'client_id': github_client_id,
                'secret': github_secret,
            }
        )
        
        if not created:
            # Actualizar si ya existe
            github_app.client_id = github_client_id
            github_app.secret = github_secret
            github_app.save()
            print("✓ GitHub OAuth actualizado")
        else:
            print("✓ GitHub OAuth creado")
        
        # Asociar con el sitio actual
        if site not in github_app.sites.all():
            github_app.sites.add(site)
            print(f"  - Asociado con el sitio {site.domain}")
    else:
        print("✗ GitHub OAuth: Faltan credenciales en .env (OAUTH_GITHUB_ID, OAUTH_GITHUB_SECRET)")
    
    print("\n¡Configuración completada!")
    print("Ahora puedes usar las opciones de login social en tu aplicación.")

if __name__ == '__main__':
    setup_social_apps()
