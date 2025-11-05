from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('history/', views.order_history, name='order_history'),
    path('create/', views.create_order, name='create_order'),
    path('<uuid:order_id>/', views.order_detail, name='order_detail'),
    path('<uuid:order_id>/cancel/', views.cancel_order, name='cancel_order'),
    
    # URLs para administradores
    path('admin/orders/', views.admin_order_list, name='admin_order_list'),
    path('admin/orders/<uuid:order_id>/', views.admin_order_detail, name='admin_order_detail'),
    path('admin/orders/<uuid:order_id>/update/', views.admin_order_update, name='admin_order_update'),
]