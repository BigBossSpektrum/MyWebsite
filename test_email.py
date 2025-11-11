#!/usr/bin/env python
"""
Script para probar la configuración de email de Zultech
Ejecutar: python test_email.py
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Zultech_main.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

def test_email_config():
    print("=" * 70)
    print("🔧 PRUEBA DE CONFIGURACIÓN DE EMAIL - ZULTECH")
    print("=" * 70)
    print()
    
    # Mostrar configuración actual
    print("📋 Configuración actual:")
    print(f"   EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
    
    if hasattr(settings, 'EMAIL_HOST'):
        print(f"   EMAIL_HOST: {settings.EMAIL_HOST}")
        print(f"   EMAIL_PORT: {settings.EMAIL_PORT}")
        print(f"   EMAIL_USE_TLS: {getattr(settings, 'EMAIL_USE_TLS', False)}")
        print(f"   EMAIL_HOST_USER: {settings.EMAIL_HOST_USER if settings.EMAIL_HOST_USER else '(no configurado)'}")
        print(f"   EMAIL_HOST_PASSWORD: {'***configurada***' if settings.EMAIL_HOST_PASSWORD else '(no configurada)'}")
    
    print(f"   DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
    print()
    
    # Verificar tipo de backend
    if 'console' in settings.EMAIL_BACKEND.lower():
        print("✅ Modo: DESARROLLO (Console Backend)")
        print("   Los emails se mostrarán en la consola, no se enviarán realmente.")
        print()
    else:
        print("✅ Modo: PRODUCCIÓN (SMTP Backend)")
        print("   Los emails se enviarán por SMTP.")
        print()
        
        # Verificar credenciales
        if not settings.EMAIL_HOST_USER or not settings.EMAIL_HOST_PASSWORD:
            print("⚠️  ADVERTENCIA: EMAIL_HOST_USER o EMAIL_HOST_PASSWORD no configurados")
            print("   Los emails probablemente fallarán.")
            print()
    
    # Preguntar si desea enviar un email de prueba
    email_destino = input("📧 Ingresa un email para enviar una prueba (Enter para omitir): ").strip()
    
    if email_destino:
        print()
        print(f"📤 Enviando email de prueba a: {email_destino}")
        
        try:
            send_mail(
                subject='🎉 Prueba de Email - Zultech',
                message='Este es un email de prueba del sistema Zultech.\n\n'
                        'Si recibes este mensaje, la configuración de email está funcionando correctamente.\n\n'
                        '¡Saludos!\n'
                        'Equipo Zultech',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email_destino],
                fail_silently=False,
            )
            print()
            print("✅ ¡Email enviado exitosamente!")
            
            if 'console' in settings.EMAIL_BACKEND.lower():
                print("   Revisa la consola arriba para ver el contenido del email.")
            else:
                print(f"   Revisa la bandeja de entrada de {email_destino}")
                print("   (También revisa la carpeta de spam)")
            
        except Exception as e:
            print()
            print("❌ Error al enviar el email:")
            print(f"   {type(e).__name__}: {str(e)}")
            print()
            print("💡 Posibles soluciones:")
            print("   1. Verifica tu archivo .env")
            print("   2. Para Gmail: usa una contraseña de aplicación")
            print("   3. Verifica que EMAIL_HOST y EMAIL_PORT sean correctos")
            print("   4. Revisa EMAIL_CONFIG.md para más ayuda")
    
    print()
    print("=" * 70)
    print("✅ Prueba completada")
    print("=" * 70)

if __name__ == '__main__':
    test_email_config()
