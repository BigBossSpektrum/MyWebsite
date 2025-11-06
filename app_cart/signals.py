"""
Signals para el manejo automático del carrito
"""
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .utils import migrate_session_cart_to_db


@receiver(user_logged_in)
def merge_cart_on_login(sender, request, user, **kwargs):
    """
    Cuando un usuario inicia sesión, migra su carrito de sesión
    al carrito de base de datos asociado a su cuenta
    """
    migrate_session_cart_to_db(request)
