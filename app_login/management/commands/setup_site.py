"""
Management command to setup Site for django.contrib.sites
This is required for django-allauth to work properly
"""
from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from django.conf import settings


class Command(BaseCommand):
    help = 'Setup Site object for django.contrib.sites'

    def handle(self, *args, **options):
        site_id = getattr(settings, 'SITE_ID', 1)
        domain = 'mywebsite-tlxs.onrender.com'
        name = 'Zultech'
        
        try:
            site, created = Site.objects.get_or_create(
                id=site_id,
                defaults={'domain': domain, 'name': name}
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✓ Site created: {site.name} ({site.domain})'
                    )
                )
            else:
                # Update if needed
                if site.domain != domain or site.name != name:
                    site.domain = domain
                    site.name = name
                    site.save()
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'✓ Site updated: {site.name} ({site.domain})'
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'✓ Site already exists: {site.name} ({site.domain})'
                        )
                    )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'✗ Error setting up site: {str(e)}')
            )
            raise
