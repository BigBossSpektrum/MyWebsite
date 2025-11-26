from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from allauth.socialaccount.models import SocialAccount
import requests
import logging

logger = logging.getLogger(__name__)
User = get_user_model()


class Command(BaseCommand):
    help = 'Actualiza las fotos de perfil de usuarios de cuentas sociales'

    def add_arguments(self, parser):
        parser.add_argument(
            '--provider',
            type=str,
            help='Proveedor específico (google, github, facebook)',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Forzar actualización incluso si ya tienen foto',
        )
        parser.add_argument(
            '--username',
            type=str,
            help='Actualizar solo un usuario específico',
        )

    def handle(self, *args, **options):
        provider = options.get('provider')
        force = options.get('force', False)
        username = options.get('username')

        # Filtrar cuentas sociales
        social_accounts = SocialAccount.objects.all()
        
        if provider:
            social_accounts = social_accounts.filter(provider=provider)
            self.stdout.write(f'Filtrando por proveedor: {provider}')
        
        if username:
            social_accounts = social_accounts.filter(user__username=username)
            self.stdout.write(f'Filtrando por usuario: {username}')

        self.stdout.write(f'Encontradas {social_accounts.count()} cuentas sociales')

        updated = 0
        skipped = 0
        errors = 0

        for social_account in social_accounts:
            user = social_account.user
            extra_data = social_account.extra_data

            # Verificar si ya tiene foto y no es forzado
            if user.Foto_Perfil and not force:
                skipped += 1
                self.stdout.write(
                    self.style.WARNING(
                        f'⏭ {user.username} ya tiene foto de perfil'
                    )
                )
                continue

            # Obtener URL de la imagen según el proveedor
            picture_url = None
            
            if social_account.provider == 'google':
                picture_url = extra_data.get('picture')
            elif social_account.provider == 'github':
                picture_url = extra_data.get('avatar_url')
            elif social_account.provider == 'facebook':
                picture_url = extra_data.get('picture', {}).get('data', {}).get('url')

            if not picture_url:
                self.stdout.write(
                    self.style.WARNING(
                        f'⚠ No se encontró URL de imagen para {user.username} ({social_account.provider})'
                    )
                )
                skipped += 1
                continue

            # Descargar y guardar la imagen
            try:
                self.stdout.write(f'📥 Descargando foto para {user.username}...')
                self.stdout.write(f'   URL: {picture_url}')
                
                response = requests.get(picture_url, timeout=10)
                
                if response.status_code == 200:
                    file_name = f"profile_{user.username}.jpg"
                    
                    # Eliminar foto anterior si existe y es forzado
                    if user.Foto_Perfil and force:
                        user.Foto_Perfil.delete(save=False)
                    
                    user.Foto_Perfil.save(
                        file_name,
                        ContentFile(response.content),
                        save=True
                    )
                    
                    updated += 1
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'✅ Foto actualizada para {user.username}'
                        )
                    )
                else:
                    errors += 1
                    self.stdout.write(
                        self.style.ERROR(
                            f'❌ Error HTTP {response.status_code} para {user.username}'
                        )
                    )
            except Exception as e:
                errors += 1
                self.stdout.write(
                    self.style.ERROR(
                        f'❌ Error al descargar foto para {user.username}: {str(e)}'
                    )
                )

        # Resumen
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS(f'✅ Actualizadas: {updated}'))
        self.stdout.write(self.style.WARNING(f'⏭ Omitidas: {skipped}'))
        self.stdout.write(self.style.ERROR(f'❌ Errores: {errors}'))
        self.stdout.write('='*50)
