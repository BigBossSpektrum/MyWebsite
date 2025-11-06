from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    # URLs para clientes
    path('', views.product_list, name='product_list'),
    path('<slug:slug>/', views.product_detail, name='product_detail'),
    
    # URLs para administradores
    path('admin/products/', views.admin_product_list, name='admin_product_list'),
    path('admin/products/create/', views.admin_product_create, name='admin_product_create'),
    path('admin/products/<uuid:product_id>/edit/', views.admin_product_edit, name='admin_product_edit'),
    path('admin/products/<uuid:product_id>/delete/', views.admin_product_delete, name='admin_product_delete'),
    path('admin/products/<uuid:product_id>/images/', views.admin_product_images, name='admin_product_images'),
    path('admin/products/<uuid:product_id>/images/upload/', views.admin_product_images_upload, name='admin_product_images_upload'),
    path('admin/products/<uuid:product_id>/images/<uuid:image_id>/update/', views.admin_product_image_update, name='admin_product_image_update'),
    path('admin/products/<uuid:product_id>/images/<uuid:image_id>/delete/', views.admin_product_image_delete, name='admin_product_image_delete'),
]