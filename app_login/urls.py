from django.urls import path
from . import views

app_name = 'login'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('register/', views.register_view, name='register'),
    path('admin/dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('admin/users/', views.admin_users_view, name='admin_users'),
    path('customer/dashboard/', views.customer_dashboard_view, name='customer_dashboard'),
    path('', views.redirect_to_dashboard, name='user_home'),
]