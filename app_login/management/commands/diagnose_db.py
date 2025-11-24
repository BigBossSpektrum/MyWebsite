"""
Django management command to diagnose database configuration
Useful for debugging deployment issues on Render
"""
from django.core.management.base import BaseCommand
from django.conf import settings
import os


class Command(BaseCommand):
    help = 'Diagnose database configuration for deployment'

    def handle(self, *args, **options):
        self.stdout.write("=" * 70)
        self.stdout.write(self.style.SUCCESS("DATABASE CONFIGURATION DIAGNOSTICS"))
        self.stdout.write("=" * 70)
        self.stdout.write("")
        
        # Environment variables
        self.stdout.write(self.style.WARNING("Environment Variables:"))
        database_url = os.environ.get('DATABASE_URL')
        if database_url:
            # Mask password for security
            masked_url = database_url
            try:
                if '@' in masked_url and '://' in masked_url:
                    protocol = masked_url.split('://')[0]
                    rest = masked_url.split('://')[1]
                    if '@' in rest:
                        credentials, host = rest.split('@', 1)
                        if ':' in credentials:
                            user = credentials.split(':')[0]
                            masked_url = f"{protocol}://{user}:***@{host}"
            except Exception:
                pass  # If masking fails, show partial URL
            self.stdout.write(f"  DATABASE_URL: {masked_url}")
        else:
            self.stdout.write(self.style.ERROR("  DATABASE_URL: Not set!"))
        
        self.stdout.write(f"  DEBUG: {os.environ.get('DEBUG', 'Not set')}")
        self.stdout.write(f"  RENDER: {os.environ.get('RENDER', 'Not set')}")
        self.stdout.write("")
        
        # Database settings
        self.stdout.write(self.style.WARNING("Django Database Configuration:"))
        db_config = settings.DATABASES['default']
        self.stdout.write(f"  Engine: {db_config['ENGINE']}")
        self.stdout.write(f"  Name: {db_config.get('NAME', 'N/A')}")
        self.stdout.write(f"  Host: {db_config.get('HOST', 'N/A')}")
        self.stdout.write(f"  Port: {db_config.get('PORT', 'N/A')}")
        self.stdout.write(f"  User: {db_config.get('USER', 'N/A')}")
        self.stdout.write("")
        
        # Test connection
        self.stdout.write(self.style.WARNING("Testing Database Connection:"))
        try:
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                if result:
                    self.stdout.write(self.style.SUCCESS("  ✓ Database connection successful!"))
                    
                    # Check if it's PostgreSQL or SQLite
                    if 'postgresql' in db_config['ENGINE']:
                        self.stdout.write(self.style.SUCCESS("  ✓ Using PostgreSQL (Production)"))
                    elif 'sqlite' in db_config['ENGINE']:
                        self.stdout.write(self.style.WARNING("  ⚠ Using SQLite (Development)"))
                    
                    # Check for django_site table
                    cursor.execute(
                        "SELECT COUNT(*) FROM information_schema.tables WHERE table_name='django_site'"
                        if 'postgresql' in db_config['ENGINE']
                        else "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='django_site'"
                    )
                    count = cursor.fetchone()[0]
                    if count > 0:
                        self.stdout.write(self.style.SUCCESS("  ✓ django_site table exists"))
                    else:
                        self.stdout.write(self.style.ERROR("  ✗ django_site table missing - Run migrations!"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"  ✗ Database connection failed: {str(e)}"))
        
        self.stdout.write("")
        self.stdout.write("=" * 70)
        
        # Recommendations
        if not database_url:
            self.stdout.write(self.style.ERROR("ISSUE DETECTED: DATABASE_URL not set!"))
            self.stdout.write("")
            self.stdout.write("Possible causes:")
            self.stdout.write("  1. Database not created in Render Dashboard")
            self.stdout.write("  2. Database not linked to web service")
            self.stdout.write("  3. Environment variable not synced")
            self.stdout.write("")
            self.stdout.write("Solution:")
            self.stdout.write("  1. Go to Render Dashboard")
            self.stdout.write("  2. Create a PostgreSQL database")
            self.stdout.write("  3. Link it to your web service")
            self.stdout.write("  4. Redeploy the service")
        elif 'sqlite' in db_config['ENGINE']:
            self.stdout.write(self.style.WARNING("WARNING: Using SQLite in what should be production!"))
            self.stdout.write("")
            self.stdout.write("This means DATABASE_URL is not being parsed correctly.")
            self.stdout.write("Check that dj-database-url is installed and DATABASE_URL format is correct.")
