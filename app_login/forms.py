from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    Correo_Electronico = forms.EmailField(required=True)
    first_name = forms.CharField(required=True, label='Nombre')
    last_name = forms.CharField(required=True, label='Apellido')
    Telefono = forms.CharField(required=False, label='Teléfono')
    Direccion = forms.CharField(required=False, label='Dirección')
    Ciudad = forms.CharField(required=False, label='Ciudad')
    Estado = forms.CharField(required=False, label='Estado/Provincia')
    Codigo_Postal = forms.CharField(required=False, label='Código Postal')
    Fecha_de_Nacimiento = forms.DateField(
        required=False, 
        label='Fecha de Nacimiento',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    Foto_Perfil = forms.ImageField(
        required=False, 
        label='Foto de Perfil',
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )

    role = forms.ChoiceField(
        choices=CustomUser.Roles.choices,
        initial=CustomUser.Roles.CUSTOMER,
        label='Tipo de Usuario',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'Correo_Electronico', 'first_name', 'last_name', 'role', 'Telefono',
                 'Direccion', 'Ciudad', 'Estado', 'Codigo_Postal', 'Fecha_de_Nacimiento',
                 'Foto_Perfil', 'password1', 'password2')