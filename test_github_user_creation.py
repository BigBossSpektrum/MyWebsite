"""
Script para probar manualmente la creación de usuario desde GitHub
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Zultech_main.settings')
django.setup()

from django.contrib.auth import get_user_model
from allauth.socialaccount.models import SocialAccount, SocialApp
from django.contrib.sites.models import Site

User = get_user_model()

print("=== TEST MANUAL DE CREACIÓN DE USUARIO ===\n")

# Simular datos que vendría de GitHub
github_data = {
    'login': 'test_github_user',
    'id': 12345678,
    'email': None,  # GitHub puede no proveer email
    'name': 'Test User',
}

print(f"1. Datos simulados de GitHub: {github_data}")

# Intentar crear usuario manualmente como lo haría allauth
try:
    # Verificar si ya existe una cuenta social con ese UID
    uid = str(github_data['id'])
    existing = SocialAccount.objects.filter(provider='github', uid=uid).first()
    
    if existing:
        print(f"\n✓ Ya existe cuenta social para UID {uid}")
        print(f"  Usuario: {existing.user.username}")
    else:
        print(f"\n2. No existe cuenta social, creando usuario...")
        
        # Crear usuario
        username = github_data['login']
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{github_data['login']}{counter}"
            counter += 1
        
        email = github_data.get('email') or f"{uid}@github.local"
        
        user = User.objects.create(
            username=username,
            email=email,
            first_name=github_data.get('name', '').split()[0] if github_data.get('name') else '',
            role='CUSTOMER'
        )
        print(f"  ✓ Usuario creado: {user.username}")
        
        # Crear cuenta social
        site = Site.objects.get_current()
        social_app = SocialApp.objects.get(provider='github')
        
        social_account = SocialAccount.objects.create(
            user=user,
            provider='github',
            uid=uid,
            extra_data=github_data
        )
        print(f"  ✓ Cuenta social creada")
        
        print(f"\n✅ ÉXITO: Usuario {user.username} creado correctamente")
        print(f"   Email: {user.email}")
        print(f"   UID de GitHub: {uid}")
        
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()

print("\n=== FIN DEL TEST ===")
