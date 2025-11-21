"""
Script para limpiar configuraciones antiguas de SocialApp en la base de datos.
Como ahora usamos configuración interna, ya no necesitamos estos registros.

OPCIONAL: Solo ejecuta este script si quieres limpiar la base de datos.
"""

import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Zultech_main.settings')
django.setup()

from allauth.socialaccount.models import SocialApp, SocialAccount, SocialToken

def clean_old_socialapp_config():
    """Limpia configuraciones antiguas de SocialApp."""
    
    print("\n" + "="*60)
    print("LIMPIEZA DE CONFIGURACIONES ANTIGUAS DE OAUTH")
    print("="*60)
    
    print("\nℹ️  Nota: Como ahora usas configuración interna,")
    print("   ya no necesitas registros de SocialApp en la base de datos.")
    
    # Contar registros existentes
    socialapp_count = SocialApp.objects.count()
    socialaccount_count = SocialAccount.objects.count()
    socialtoken_count = SocialToken.objects.count()
    
    print("\n" + "-"*60)
    print("REGISTROS ACTUALES EN LA BASE DE DATOS")
    print("-"*60)
    print(f"SocialApp (credenciales OAuth): {socialapp_count}")
    print(f"SocialAccount (cuentas sociales de usuarios): {socialaccount_count}")
    print(f"SocialToken (tokens de acceso): {socialtoken_count}")
    
    if socialapp_count == 0:
        print("\n✅ No hay registros de SocialApp para limpiar.")
        print("   Tu base de datos ya está limpia.")
        return
    
    # Mostrar los SocialApp existentes
    print("\n" + "-"*60)
    print("SOCIALAPP ENCONTRADOS")
    print("-"*60)
    
    for app in SocialApp.objects.all():
        print(f"\nProveedor: {app.provider}")
        print(f"  Nombre: {app.name}")
        print(f"  Client ID: {app.client_id[:20]}...")
        print(f"  Sitios: {', '.join([str(site) for site in app.sites.all()])}")
    
    # Preguntar si quiere eliminar
    print("\n" + "-"*60)
    print("⚠️  ¿DESEAS ELIMINAR ESTOS REGISTROS?")
    print("-"*60)
    print("\nℹ️  Información importante:")
    print("  • Las credenciales ahora están en settings.py (variables de entorno)")
    print("  • Eliminar SocialApp NO afecta el funcionamiento del OAuth")
    print("  • Los usuarios y sus cuentas sociales NO se eliminarán")
    print("  • Solo se eliminan las credenciales almacenadas en la BD")
    
    respuesta = input("\n¿Eliminar registros de SocialApp? (s/n): ").lower().strip()
    
    if respuesta == 's':
        print("\n🗑️  Eliminando registros de SocialApp...")
        
        deleted = SocialApp.objects.all().delete()
        
        print(f"\n✓ Eliminados: {deleted[0]} registros")
        print("\n✅ Base de datos limpiada correctamente.")
        print("\nℹ️  Recuerda: Las credenciales OAuth ahora están en:")
        print("   - settings.py → SOCIALACCOUNT_PROVIDERS")
        print("   - .env → OAUTH_GOOGLE_ID, OAUTH_GOOGLE_SECRET, etc.")
        
    else:
        print("\n❌ Cancelado. No se eliminaron registros.")
        print("\nℹ️  Puedes mantener los registros de SocialApp sin problemas.")
        print("   La configuración interna tiene prioridad sobre la base de datos.")
    
    # Mostrar estado final
    print("\n" + "-"*60)
    print("ESTADO FINAL")
    print("-"*60)
    
    final_count = SocialApp.objects.count()
    print(f"SocialApp en base de datos: {final_count}")
    
    if final_count == 0:
        print("✓ Base de datos limpia")
        print("✓ Usando configuración interna de settings.py")
    else:
        print("ℹ️  SocialApp todavía en base de datos (no afecta funcionamiento)")
        print("✓ Configuración interna tiene prioridad")
    
    print("\n" + "="*60)
    print("LIMPIEZA COMPLETADA")
    print("="*60 + "\n")

if __name__ == '__main__':
    try:
        clean_old_socialapp_config()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
