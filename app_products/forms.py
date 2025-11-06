from django import forms
from .models import Product, Category


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'slug', 'description', 'category', 'price', 'stock', 'available']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del producto'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'slug-del-producto'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Descripción del producto'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'name': 'Nombre',
            'slug': 'Slug (URL)',
            'description': 'Descripción',
            'category': 'Categoría',
            'price': 'Precio',
            'stock': 'Stock',
            'available': 'Disponible',
        }
        help_texts = {
            'slug': 'URL amigable para el producto (ej: producto-ejemplo)',
            'price': 'Precio en la moneda local',
            'stock': 'Cantidad disponible en inventario',
        }
