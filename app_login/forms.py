from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    Correo_Electronico = forms.EmailField(
        required=True, 
        label='Correo Electrónico',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    first_name = forms.CharField(
        required=True, 
        label='Nombre',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        required=True, 
        label='Apellido',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    Telefono = forms.CharField(
        required=False, 
        label='Teléfono',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    Direccion = forms.CharField(
        required=False, 
        label='Dirección',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    Ciudad = forms.CharField(
        required=False, 
        label='Ciudad',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    Estado = forms.CharField(
        required=False, 
        label='Estado/Provincia',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    Codigo_Postal = forms.CharField(
        required=False, 
        label='Código Postal',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    Fecha_de_Nacimiento = forms.DateField(
        required=False, 
        label='Fecha de Nacimiento',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    Foto_Perfil = forms.ImageField(
        required=False, 
        label='Foto de Perfil',
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'Correo_Electronico', 'first_name', 'last_name', 'Telefono',
                 'Direccion', 'Ciudad', 'Estado', 'Codigo_Postal', 'Fecha_de_Nacimiento',
                 'Foto_Perfil', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['Correo_Electronico']
        user.role = CustomUser.Roles.CUSTOMER  # Siempre registrar como cliente
        if commit:
            user.save()
        return user