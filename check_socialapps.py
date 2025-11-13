#!/usr/bin/env python
"""Script para verificar configuración de SocialApp"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Zultech_main.settings')
django.setup()

from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site

print("Verificando configuración de SocialApp y Sites...\n")

# Verificar Sites
sites = Site.objects.all()
print(f"Sites configurados: {sites.count()}")
for site in sites:
    print(f"  - ID: {site.id}, Domain: {site.domain}, Name: {site.name}")

print("\n" + "="*50 + "\n")

# Verificar SocialApps
social_apps = SocialApp.objects.all()
print(f"SocialApps configurados: {social_apps.count()}")
for app in social_apps:
    print(f"\n  Provider: {app.provider}")
    print(f"  Name: {app.name}")
    print(f"  Client ID: {app.client_id[:30]}...")
    print(f"  Sites asociados: {list(app.sites.values_list('domain', flat=True))}")

# Verificar SITE_ID
from django.conf import settings
print(f"\n" + "="*50)
print(f"SITE_ID en settings: {settings.SITE_ID}")

# Verificar si hay conflicto
google_apps = SocialApp.objects.filter(provider='google')
if google_apps.count() > 1:
    print(f"\n⚠ PROBLEMA: Hay {google_apps.count()} apps de Google configuradas")
    print("Se debe mantener solo una.")
else:
    print("\n✓ Configuración correcta: 1 app de Google")
