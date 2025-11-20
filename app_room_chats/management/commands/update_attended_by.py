from django.core.management.base import BaseCommand
from django.utils import timezone
from app_room_chats.models import ChatRoom


class Command(BaseCommand):
    help = 'Actualiza el campo attended_by para chats que tienen admin pero no attended_by'

    def handle(self, *args, **options):
        # Buscar chats con admin asignado pero sin attended_by
        chats_to_update = ChatRoom.objects.filter(
            admin__isnull=False,
            attended_by__isnull=True
        )
        
        count = chats_to_update.count()
        
        if count == 0:
            self.stdout.write(
                self.style.WARNING('No hay chats para actualizar.')
            )
            return
        
        self.stdout.write(
            self.style.NOTICE(f'Encontrados {count} chat(s) para actualizar...')
        )
        
        # Actualizar cada chat
        updated = 0
        for chat in chats_to_update:
            chat.attended_by = chat.admin
            # Si no tiene attended_at, usar la fecha de creación o actualización
            if not chat.attended_at:
                chat.attended_at = chat.updated_at or chat.created_at
            chat.save()
            updated += 1
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'✓ Chat {chat.id} actualizado: attended_by={chat.attended_by.email}'
                )
            )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n¡Completado! {updated} chat(s) actualizado(s) exitosamente.'
            )
        )
