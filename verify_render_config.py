#!/usr/bin/env python
"""
Script to verify Render deployment configuration
Run this before deploying to catch common issues
"""
import os
import sys
from pathlib import Path

# Add project to path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Zultech_main.settings')

import django
django.setup()

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.management import call_command

def check_database():
    """Verify database configuration"""
    print("🔍 Checking database configuration...")
    db_config = settings.DATABASES['default']
    
    if 'DATABASE_URL' in os.environ:
        print("✅ Using PostgreSQL (DATABASE_URL detected)")
        print(f"   Engine: {db_config['ENGINE']}")
    else:
        print("⚠️  Using SQLite (local development)")
        print(f"   Database: {db_config['NAME']}")
    print()

def check_migrations():
    """Check if migrations are applied"""
    print("🔍 Checking migrations...")
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='django_site'"
            )
            result = cursor.fetchone()
            if result:
                print("✅ django_site table exists")
            else:
                print("❌ django_site table missing - run migrations!")
                return False
    except Exception as e:
        print(f"⚠️  Could not check migrations: {e}")
    print()
    return True

def check_site():
    """Verify Site object exists"""
    print("🔍 Checking Site object...")
    try:
        site = Site.objects.get(id=settings.SITE_ID)
        print(f"✅ Site exists: {site.name} ({site.domain})")
        
        if 'mywebsite-tlxs.onrender.com' in site.domain or site.domain == 'localhost':
            print("   Domain looks good!")
        else:
            print(f"⚠️  Domain might need updating: {site.domain}")
    except Site.DoesNotExist:
        print("❌ Site object missing!")
        print("   Run: python manage.py setup_site")
        return False
    except Exception as e:
        print(f"⚠️  Error checking site: {e}")
    print()
    return True

def check_static_files():
    """Verify static files configuration"""
    print("🔍 Checking static files...")
    print(f"   STATIC_URL: {settings.STATIC_URL}")
    print(f"   STATIC_ROOT: {settings.STATIC_ROOT}")
    
    if settings.STATICFILES_STORAGE == 'whitenoise.storage.CompressedManifestStaticFilesStorage':
        print("✅ WhiteNoise configured")
    else:
        print(f"⚠️  Static files storage: {settings.STATICFILES_STORAGE}")
    print()

def check_oauth():
    """Check OAuth configuration"""
    print("🔍 Checking OAuth configuration...")
    
    providers = {
        'Google': ('OAUTH_GOOGLE_ID', 'OAUTH_GOOGLE_SECRET'),
        'GitHub': ('OAUTH_GITHUB_ID', 'OAUTH_GITHUB_SECRET'),
        'Facebook': ('OAUTH_FACEBOOK_ID', 'OAUTH_FACEBOOK_SECRET'),
    }
    
    for name, (id_key, secret_key) in providers.items():
        client_id = os.environ.get(id_key, '')
        secret = os.environ.get(secret_key, '')
        
        if client_id and secret:
            print(f"✅ {name} OAuth configured")
        else:
            print(f"⚠️  {name} OAuth not configured (optional)")
    print()

def check_security():
    """Check security settings"""
    print("🔍 Checking security settings...")
    
    if settings.DEBUG:
        print("⚠️  DEBUG is True - should be False in production!")
    else:
        print("✅ DEBUG is False")
    
    if settings.SECRET_KEY == 'django-insecure-9%5%^u$mc8fyb+t8^x&5l%+rm*&49erq#mdesn1yap2q2b1q=k':
        print("⚠️  Using default SECRET_KEY - should be changed in production!")
    else:
        print("✅ SECRET_KEY is set")
    
    print(f"   ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
    print()

def check_requirements():
    """Check if all required packages are in requirements.txt"""
    print("🔍 Checking requirements.txt...")
    
    required_packages = [
        'Django',
        'gunicorn',
        'dj-database-url',
        'psycopg2-binary',
        'whitenoise',
        'django-allauth',
        'channels',
        'daphne',
        'uvicorn',
    ]
    
    req_file = BASE_DIR / 'requirements.txt'
    if req_file.exists():
        with open(req_file, 'r') as f:
            content = f.read().lower()
            
        missing = []
        for pkg in required_packages:
            if pkg.lower() not in content:
                missing.append(pkg)
        
        if missing:
            print(f"❌ Missing packages in requirements.txt: {', '.join(missing)}")
            return False
        else:
            print("✅ All required packages in requirements.txt")
    else:
        print("❌ requirements.txt not found!")
        return False
    print()
    return True

def check_build_script():
    """Check if build.sh exists and is valid"""
    print("🔍 Checking build.sh...")
    
    build_file = BASE_DIR / 'build.sh'
    if build_file.exists():
        with open(build_file, 'r') as f:
            content = f.read()
        
        required_commands = ['migrate', 'collectstatic', 'setup_site']
        missing = []
        
        for cmd in required_commands:
            if cmd not in content:
                missing.append(cmd)
        
        if missing:
            print(f"⚠️  Missing commands in build.sh: {', '.join(missing)}")
        else:
            print("✅ build.sh looks good")
    else:
        print("❌ build.sh not found!")
        return False
    print()
    return True

def main():
    """Run all checks"""
    print("=" * 60)
    print("🚀 Render Deployment Verification")
    print("=" * 60)
    print()
    
    checks = [
        check_requirements,
        check_build_script,
        check_database,
        check_security,
        check_static_files,
        check_oauth,
    ]
    
    # Only check migrations and site if database is available
    try:
        if check_migrations():
            checks.append(check_site)
    except Exception:
        print("⚠️  Database not available - skipping migration checks")
    
    print("=" * 60)
    print("📋 Summary")
    print("=" * 60)
    print()
    
    all_passed = all(check() if callable(check) else True for check in checks)
    
    if all_passed:
        print("✅ All checks passed! Ready to deploy to Render.")
    else:
        print("⚠️  Some checks failed. Please fix the issues above.")
    
    print()
    print("Next steps:")
    print("1. Push your code to GitHub")
    print("2. Create/update service on Render")
    print("3. Configure environment variables in Render Dashboard")
    print("4. Wait for build to complete")
    print()

if __name__ == '__main__':
    main()
