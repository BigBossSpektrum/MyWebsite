from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class CustomUser(AbstractUser):
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="El número de teléfono debe estar en el formato: '+999999999'. Hasta 15 dígitos permitidos."
    )
    
    # Campos personalizados
    Telefono = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    Direccion = models.CharField(max_length=255, blank=True)
    Ciudad = models.CharField(max_length=100, blank=True)
    Estado = models.CharField(max_length=100, blank=True)
    Codigo_Postal = models.CharField(max_length=10, blank=True)
    Fecha_de_Nacimiento = models.DateField(null=True, blank=True)
    Foto_Perfil = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return self.username
