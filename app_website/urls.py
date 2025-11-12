from django.urls import path
from . import views

app_name = 'website'

urlpatterns = [
    path('', views.Dashboard, name='Dashboard'),
    path('contacto/', views.contact, name='contact'),
]
