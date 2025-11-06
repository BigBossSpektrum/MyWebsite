from django.apps import AppConfig


class AppCartConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_cart'
    verbose_name = 'Carrito de Compras'

    def ready(self):
        """Importar signals cuando la app esté lista"""
        import app_cart.signals
