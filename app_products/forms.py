from django import forms
from .models import Product, Category, ProductImage


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'slug', 'description', 'category', 'price', 'stock', 'available']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del producto'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'slug-del-producto'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Descripción del producto'}),
            'category': forms.Select(attrs={
                'class': 'form-control custom-select',
            }),
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
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Agregar opción vacía al select de categoría
        self.fields['category'].empty_label = "-- Selecciona una categoría --"
        # Agregar clase is-invalid si hay errores
        for field_name, field in self.fields.items():
            if self.errors.get(field_name):
                if 'class' in field.widget.attrs:
                    field.widget.attrs['class'] += ' is-invalid'
                else:
                    field.widget.attrs['class'] = 'is-invalid'


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image', 'alt_text', 'is_main']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'alt_text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Texto alternativo para la imagen'}),
            'is_main': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'image': 'Imagen',
            'alt_text': 'Texto Alternativo',
            'is_main': 'Imagen Principal',
        }
        help_texts = {
            'alt_text': 'Descripción de la imagen para accesibilidad',
            'is_main': 'Marcar como imagen principal del producto',
        }
