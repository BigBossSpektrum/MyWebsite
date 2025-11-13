from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.utils import perform_login
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.core.files.base import ContentFile
import requests

User = get_user_model()

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    Adaptador personalizado para manejar la autenticación social.
    Crea automáticamente cuentas de usuario si no existen.
    """
    
    def pre_social_login(self, request, sociallogin):
        """
        Se ejecuta antes del login social.
        Conecta cuentas sociales con usuarios existentes basándose en el email.
        """
        # Si el usuario ya está autenticado, no hacemos nada
        if sociallogin.is_existing:
            return
        
        # Intentar obtener el email de la cuenta social
        email = None
        if sociallogin.account.extra_data.get('email'):
            email = sociallogin.account.extra_data['email']
        
        if not email:
            return
        
        # Buscar si existe un usuario con ese email
        try:
            user = User.objects.get(email=email)
            # Conectar la cuenta social con el usuario existente
            sociallogin.connect(request, user)
        except User.DoesNotExist:
            # El usuario no existe, se creará automáticamente
            pass
    
    def save_user(self, request, sociallogin, form=None):
        """
        Guarda un nuevo usuario desde una cuenta social.
        Personaliza la creación del usuario con datos de la cuenta social.
        """
        user = super().save_user(request, sociallogin, form)
        
        # Extraer datos adicionales del proveedor social
        extra_data = sociallogin.account.extra_data
        
        # Configurar correo electrónico
        if extra_data.get('email'):
            user.email = extra_data.get('email')
            user.Correo_Electronico = extra_data.get('email')
        
        # Configurar campos adicionales según el proveedor
        if not user.first_name and extra_data.get('first_name'):
            user.first_name = extra_data.get('first_name', '')
        
        if not user.last_name and extra_data.get('last_name'):
            user.last_name = extra_data.get('last_name', '')
        
        # Si el nombre completo viene en un solo campo (como en Google)
        if not user.first_name and not user.last_name and extra_data.get('name'):
            name_parts = extra_data.get('name', '').split(' ', 1)
            user.first_name = name_parts[0]
            if len(name_parts) > 1:
                user.last_name = name_parts[1]
        
        # Descargar y guardar la foto de perfil de Google
        picture_url = extra_data.get('picture')
        if picture_url and not user.Foto_Perfil:
            try:
                response = requests.get(picture_url, timeout=10)
                if response.status_code == 200:
                    # Extraer el nombre del archivo del usuario
                    file_name = f"profile_{user.username}.jpg"
                    user.Foto_Perfil.save(
                        file_name,
                        ContentFile(response.content),
                        save=False
                    )
            except Exception as e:
                # Si falla la descarga de la imagen, continuar sin ella
                print(f"Error descargando imagen de perfil: {e}")
        
        # Asignar rol de CUSTOMER por defecto para cuentas sociales
        if not user.role:
            user.role = User.Roles.CUSTOMER
        
        user.save()
        return user
    
    def get_login_redirect_url(self, request):
        """
        Redirige al usuario después del login social según su rol.
        """
        user = request.user
        
        if user.is_authenticated:
            if hasattr(user, 'is_admin') and user.is_admin():
                return '/accounts/admin/dashboard/'
            return '/accounts/customer/dashboard/'
        
        return super().get_login_redirect_url(request)
    
    def populate_user(self, request, sociallogin, data):
        """
        Puebla los datos del usuario desde los datos de la cuenta social.
        """
        user = super().populate_user(request, sociallogin, data)
        
        # Asegurarse de que el email esté configurado
        email = data.get('email') or ''
        if email:
            user.email = email
            user.Correo_Electronico = email
        
        # Configurar nombre y apellido si vienen en los datos
        if data.get('first_name'):
            user.first_name = data.get('first_name')
        if data.get('last_name'):
            user.last_name = data.get('last_name')
        
        # Si el nombre completo viene en un solo campo
        if not user.first_name and not user.last_name and data.get('name'):
            name_parts = data.get('name', '').split(' ', 1)
            user.first_name = name_parts[0]
            if len(name_parts) > 1:
                user.last_name = name_parts[1]
        
        # Configurar username si no existe
        if not user.username:
            # Usar el email como base para el username
            email_username = email.split('@')[0] if email else ''
            base_username = email_username or sociallogin.account.uid
            
            # Asegurar que el username sea único
            username = base_username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1
            
            user.username = username
        
        return user
