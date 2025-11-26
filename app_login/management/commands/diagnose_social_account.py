from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from allauth.socialaccount.models import SocialAccount
import json

User = get_user_model()


class Command(BaseCommand):
    help = 'Diagnostica la información de cuentas sociales de un usuario'

    def add_arguments(self, parser):
        parser.add_argument(
            'username',
            type=str,
            help='Username del usuario a diagnosticar',
        )

    def handle(self, *args, **options):
        username = options['username']

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'❌ Usuario "{username}" no encontrado')
            )
            return

        self.stdout.write('='*60)
        self.stdout.write(self.style.SUCCESS(f'👤 Usuario: {user.username}'))
        self.stdout.write('='*60)
        
        self.stdout.write(f'\n📧 Email: {user.email}')
        self.stdout.write(f'📧 Correo_Electronico: {user.Correo_Electronico}')
        self.stdout.write(f'👤 Nombre: {user.first_name} {user.last_name}')
        self.stdout.write(f'🎭 Role: {user.role}')
        self.stdout.write(f'📸 Foto_Perfil: {user.Foto_Perfil}')
        
        if user.Foto_Perfil:
            self.stdout.write(f'   📁 Path: {user.Foto_Perfil.path}')
            self.stdout.write(f'   🔗 URL: {user.Foto_Perfil.url}')
        else:
            self.stdout.write(self.style.WARNING('   ⚠ No tiene foto de perfil'))

        # Buscar cuentas sociales asociadas
        social_accounts = SocialAccount.objects.filter(user=user)
        
        if not social_accounts.exists():
            self.stdout.write(
                self.style.WARNING('\n⚠ No hay cuentas sociales asociadas')
            )
            return

        self.stdout.write(f'\n🔗 Cuentas sociales: {social_accounts.count()}')
        
        for social_account in social_accounts:
            self.stdout.write('\n' + '-'*60)
            self.stdout.write(f'🏢 Proveedor: {social_account.provider.upper()}')
            self.stdout.write(f'🆔 UID: {social_account.uid}')
            self.stdout.write(f'📅 Última conexión: {social_account.last_login}')
            
            self.stdout.write('\n📊 Extra Data:')
            extra_data = social_account.extra_data
            
            # Mostrar campos relevantes
            relevant_fields = ['email', 'name', 'picture', 'avatar_url', 'login', 'given_name', 'family_name']
            
            for field in relevant_fields:
                if field in extra_data:
                    value = extra_data[field]
                    if field in ['picture', 'avatar_url']:
                        self.stdout.write(self.style.SUCCESS(f'   🖼️  {field}: {value}'))
                    else:
                        self.stdout.write(f'   • {field}: {value}')
            
            # Mostrar todos los campos si hay más
            other_fields = set(extra_data.keys()) - set(relevant_fields)
            if other_fields:
                self.stdout.write('\n📋 Otros campos disponibles:')
                for field in sorted(other_fields):
                    self.stdout.write(f'   • {field}')
            
            self.stdout.write('\n🔍 JSON completo:')
            self.stdout.write(json.dumps(extra_data, indent=2, ensure_ascii=False))

        self.stdout.write('\n' + '='*60)
