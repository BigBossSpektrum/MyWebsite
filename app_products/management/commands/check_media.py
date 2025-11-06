from django.core.management.base import BaseCommand
from django.conf import settings
from app_products.models import Product, ProductImage
import os


class Command(BaseCommand):
    help = 'Verifica la configuración de archivos media y muestra información de productos con imágenes'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=== Verificación de Configuración de Media ===\n'))
        
        # Verificar configuración
        self.stdout.write(f'MEDIA_URL: {settings.MEDIA_URL}')
        self.stdout.write(f'MEDIA_ROOT: {settings.MEDIA_ROOT}')
        self.stdout.write(f'DEBUG: {settings.DEBUG}\n')
        
        # Verificar que existe la carpeta media
        if os.path.exists(settings.MEDIA_ROOT):
            self.stdout.write(self.style.SUCCESS(f'✓ Carpeta MEDIA_ROOT existe: {settings.MEDIA_ROOT}'))
        else:
            self.stdout.write(self.style.ERROR(f'✗ Carpeta MEDIA_ROOT NO existe: {settings.MEDIA_ROOT}'))
        
        # Verificar productos
        total_products = Product.objects.count()
        products_with_images = Product.objects.filter(images__isnull=False).distinct().count()
        total_images = ProductImage.objects.count()
        
        self.stdout.write(f'\n=== Estadísticas de Productos ===')
        self.stdout.write(f'Total de productos: {total_products}')
        self.stdout.write(f'Productos con imágenes: {products_with_images}')
        self.stdout.write(f'Total de imágenes: {total_images}\n')
        
        # Listar productos con sus imágenes
        if products_with_images > 0:
            self.stdout.write(self.style.SUCCESS('=== Productos con Imágenes ==='))
            for product in Product.objects.filter(images__isnull=False).distinct():
                self.stdout.write(f'\n{product.name}:')
                for img in product.images.all():
                    image_path = img.image.path if hasattr(img.image, 'path') else 'N/A'
                    exists = os.path.exists(image_path) if image_path != 'N/A' else False
                    status = '✓' if exists else '✗'
                    main = '(Principal)' if img.is_main else ''
                    self.stdout.write(f'  {status} {img.image.url} {main}')
                    if not exists and image_path != 'N/A':
                        self.stdout.write(self.style.WARNING(f'    Archivo no existe: {image_path}'))
        else:
            self.stdout.write(self.style.WARNING('\nNo hay productos con imágenes.'))
            self.stdout.write(self.style.WARNING('Para añadir imágenes, accede al admin: /admin/'))
