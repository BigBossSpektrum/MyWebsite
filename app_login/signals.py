"""
Signals para depurar el proceso de autenticación social
"""
from allauth.socialaccount.signals import pre_social_login, social_account_added
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_login_failed

@receiver(pre_social_login)
def on_pre_social_login(sender, request, sociallogin, **kwargs):
    """Se ejecuta antes del login social"""
    pass

@receiver(social_account_added)
def on_social_account_added(sender, request, sociallogin, **kwargs):
    """Se ejecuta cuando se agrega una cuenta social"""
    pass

@receiver(user_logged_in)
def on_user_logged_in(sender, request, user, **kwargs):
    """Se ejecuta cuando un usuario inicia sesión"""
    pass

@receiver(user_login_failed)
def on_user_login_failed(sender, credentials, request, **kwargs):
    """Se ejecuta cuando falla el login"""
    pass
