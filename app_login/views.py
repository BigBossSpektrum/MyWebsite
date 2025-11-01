from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from functools import wraps
from .forms import CustomUserCreationForm
from .models import CustomUser

def admin_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_admin():
            return function(request, *args, **kwargs)
        raise PermissionDenied
    return wrap

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember')
        expected_role = request.POST.get('expected_role', 'CUSTOMER')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Verificar si el rol del usuario coincide con el rol esperado
            if user.role != expected_role:
                if expected_role == 'ADMIN':
                    messages.error(request, 'Este usuario no tiene permisos de administrador.')
                else:
                    messages.error(request, 'Por favor, use el inicio de sesión de administrador.')
                return render(request, 'login.html')
            
            login(request, user)
            if not remember_me:
                request.session.set_expiry(0)
            
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            messages.success(request, f'¡Bienvenido de nuevo, {user.get_full_name() or user.username}!')
            if user.is_admin():
                return redirect('admin_dashboard')
            return redirect('customer_dashboard')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    
    return render(request, 'login.html')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '¡Registro exitoso! Bienvenido a Zultech.')
            if user.is_admin():
                return redirect('admin_dashboard')
            return redirect('customer_dashboard')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'register.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'Has cerrado sesión exitosamente.')
    return redirect('login')

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado exitosamente.')
            return redirect('profile')
    else:
        form = CustomUserCreationForm(instance=request.user)
    
    return render(request, 'profile.html', {'form': form})

@admin_required
def admin_dashboard_view(request):
    # Datos para el dashboard de administrador
    context = {
        'total_users': CustomUser.objects.count(),
        'total_products': 0,  # TODO: Obtener de app_products
        'pending_orders': 0,  # TODO: Obtener de app_orders
        'latest_users': CustomUser.objects.order_by('-date_joined')[:5],
        'latest_orders': []  # TODO: Obtener de app_orders
    }
    return render(request, 'admin/dashboard.html', context)

@login_required
def customer_dashboard_view(request):
    if request.user.is_admin():
        return redirect('admin_dashboard')
    # Datos para el dashboard de cliente
    context = {
        'total_orders': 0,  # TODO: Obtener pedidos del cliente
        'cart_items': 0,  # TODO: Obtener items en carrito
        'wishlist_items': 0  # TODO: Obtener items en lista de deseos
    }
    return render(request, 'customer/dashboard.html', context)

@admin_required
def admin_users_view(request):
    users = CustomUser.objects.all().order_by('-date_joined')
    return render(request, 'admin/users.html', {'users': users})

@login_required
def redirect_to_dashboard(request):
    if request.user.is_admin():
        return redirect('admin_dashboard')
    return redirect('customer_dashboard')