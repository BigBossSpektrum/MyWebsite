"""
Script para verificar la configuración interna de OAuth (sin admin).
Muestra las credenciales configuradas y valida que estén completas.
"""

import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Zultech_main.settings')
django.setup()

from django.conf import settings
from dotenv import load_dotenv

# Recargar variables de entorno
load_dotenv()

def verify_internal_oauth_config():
    """Verifica la configuración interna de OAuth."""
    
    print("\n" + "="*60)
    print("VERIFICACIÓN DE CONFIGURACIÓN INTERNA DE OAUTH")
    print("="*60)
    
    # Verificar que no se esté usando SITE_ID
    if hasattr(settings, 'SITE_ID'):
        print("\n⚠️  WARNING: SITE_ID está configurado.")
        print("    Con configuración interna no es necesario.")
    else:
        print("\n✓ SITE_ID no está configurado (correcto para configuración interna)")
    
    # Verificar configuración de proveedores
    print("\n" + "-"*60)
    print("PROVEEDORES CONFIGURADOS")
    print("-"*60)
    
    if hasattr(settings, 'SOCIALACCOUNT_PROVIDERS'):
        providers = settings.SOCIALACCOUNT_PROVIDERS
        
        for provider_name, config in providers.items():
            print(f"\n{provider_name.upper()}:")
            
            # Verificar si tiene configuración APP
            if 'APP' in config:
                app_config = config['APP']
                client_id = app_config.get('client_id', '')
                secret = app_config.get('secret', '')
                
                # Mostrar información
                print(f"  ✓ Configuración interna detectada")
                print(f"  Client ID: {client_id[:20]}..." if client_id else "  ❌ Client ID no configurado")
                print(f"  Secret: {'*' * 20}..." if secret else "  ❌ Secret no configurado")
                
                # Validar que las credenciales estén completas
                if client_id and secret:
                    print(f"  ✓ Credenciales completas")
                else:
                    print(f"  ❌ ERROR: Credenciales incompletas")
                    
                    # Sugerencias
                    if not client_id:
                        env_var = f"OAUTH_{provider_name.upper()}_ID"
                        print(f"     → Falta variable de entorno: {env_var}")
                    if not secret:
                        env_var = f"OAUTH_{provider_name.upper()}_SECRET"
                        print(f"     → Falta variable de entorno: {env_var}")
            else:
                print(f"  ⚠️  Configuración de base de datos (no interna)")
                print(f"     Debes agregar 'APP' con 'client_id' y 'secret'")
            
            # Mostrar scopes
            if 'SCOPE' in config:
                print(f"  Scopes: {', '.join(config['SCOPE'])}")
    else:
        print("❌ ERROR: SOCIALACCOUNT_PROVIDERS no está configurado")
    
    # Verificar variables de entorno
    print("\n" + "-"*60)
    print("VARIABLES DE ENTORNO")
    print("-"*60)
    
    env_vars = {
        'OAUTH_GOOGLE_ID': os.environ.get('OAUTH_GOOGLE_ID', ''),
        'OAUTH_GOOGLE_SECRET': os.environ.get('OAUTH_GOOGLE_SECRET', ''),
        'OAUTH_GITHUB_ID': os.environ.get('OAUTH_GITHUB_ID', ''),
        'OAUTH_GITHUB_SECRET': os.environ.get('OAUTH_GITHUB_SECRET', ''),
    }
    
    for var_name, var_value in env_vars.items():
        if var_value:
            if 'SECRET' in var_name:
                print(f"✓ {var_name}: {'*' * 20}...")
            else:
                print(f"✓ {var_name}: {var_value[:20]}...")
        else:
            print(f"❌ {var_name}: NO CONFIGURADA")
    
    # Verificar configuración de allauth
    print("\n" + "-"*60)
    print("CONFIGURACIÓN DE ALLAUTH")
    print("-"*60)
    
    allauth_settings = {
        'SOCIALACCOUNT_AUTO_SIGNUP': getattr(settings, 'SOCIALACCOUNT_AUTO_SIGNUP', None),
        'SOCIALACCOUNT_EMAIL_REQUIRED': getattr(settings, 'SOCIALACCOUNT_EMAIL_REQUIRED', None),
        'SOCIALACCOUNT_EMAIL_VERIFICATION': getattr(settings, 'SOCIALACCOUNT_EMAIL_VERIFICATION', None),
        'SOCIALACCOUNT_STORE_TOKENS': getattr(settings, 'SOCIALACCOUNT_STORE_TOKENS', None),
    }
    
    for setting_name, setting_value in allauth_settings.items():
        print(f"{setting_name}: {setting_value}")
    
    # Verificar que django.contrib.sites no esté en INSTALLED_APPS
    print("\n" + "-"*60)
    print("INSTALLED APPS")
    print("-"*60)
    
    if 'django.contrib.sites' in settings.INSTALLED_APPS:
        print("⚠️  'django.contrib.sites' está en INSTALLED_APPS")
        print("   Con configuración interna no es necesario (pero no causa problemas)")
    else:
        print("✓ 'django.contrib.sites' no está en INSTALLED_APPS (correcto)")
    
    # URLs de callback
    print("\n" + "-"*60)
    print("URLs DE CALLBACK (para configurar en los proveedores)")
    print("-"*60)
    
    allowed_hosts = settings.ALLOWED_HOSTS
    for host in allowed_hosts:
        if host and host != '*':
            print(f"\nPara {host}:")
            print(f"  Google: https://{host}/accounts/google/login/callback/")
            print(f"  GitHub: https://{host}/accounts/github/login/callback/")
    
    print("\n" + "="*60)
    print("VERIFICACIÓN COMPLETADA")
    print("="*60 + "\n")

if __name__ == '__main__':
    verify_internal_oauth_config()
