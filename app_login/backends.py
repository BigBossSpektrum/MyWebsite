from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()


class EmailOrUsernameModelBackend(ModelBackend):
    """
    Backend de autenticación personalizado que permite iniciar sesión
    con username o email.
    """
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Permite autenticación con username o email
        """
        if username is None or password is None:
            return None
        
        try:
            # Buscar usuario por username o email
            user = User.objects.get(
                Q(username=username) | Q(email=username) | Q(Correo_Electronico=username)
            )
            
            # Verificar la contraseña
            if user.check_password(password):
                return user
            
        except User.DoesNotExist:
            # Ejecutar el hasher de password para evitar timing attacks
            User().set_password(password)
            return None
        except User.MultipleObjectsReturned:
            # Si hay múltiples usuarios con el mismo email, usar el primero
            user = User.objects.filter(
                Q(username=username) | Q(email=username) | Q(Correo_Electronico=username)
            ).first()
            
            if user and user.check_password(password):
                return user
        
        return None
    
    def get_user(self, user_id):
        """
        Obtiene un usuario por su ID
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
