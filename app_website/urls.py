from django.urls import path
from . import views

app_name = 'website'

urlpatterns = [
    path('', views.Dashboard, name='Dashboard'),
    path('contacto/', views.contact, name='contact'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms-of-service/', views.terms_of_service, name='terms_of_service'),
    path('data-deletion/', views.data_deletion, name='data_deletion'),
    path('facebook/data-deletion-callback/', views.facebook_data_deletion_callback, name='facebook_data_deletion_callback'),
]
