from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    # READ - Ver carrito
    path('', views.cart_view, name='cart_view'),
    
    # CREATE - Agregar al carrito
    path('add/<uuid:product_id>/', views.add_to_cart, name='add_to_cart'),
    
    # UPDATE - Actualizar cantidad
    path('update/<uuid:product_id>/', views.update_cart, name='update_cart'),
    
    # DELETE - Eliminar item específico
    path('remove/<uuid:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    
    # DELETE - Limpiar todo el carrito
    path('clear/', views.clear_cart, name='clear_cart'),
    
    # Checkout
    path('checkout/', views.checkout, name='checkout'),
    
    # API - Obtener conteo de items (para AJAX)
    path('api/count/', views.cart_item_count, name='cart_item_count'),
]