from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
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
        if request.user.is_admin():
            return HttpResponseRedirect(reverse('login:admin_dashboard'))
        return HttpResponseRedirect(reverse('login:customer_dashboard'))
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        remember_me = request.POST.get('remember')
        expected_role = request.POST.get('expected_role', 'CUSTOMER')
        
        # Validar que los campos no estén vacíos
        if not username or not password:
            messages.error(request, 'Por favor ingresa tu usuario/email y contraseña.')
            return render(request, 'login.html')
        
        # Autenticar usuario (el backend personalizado maneja username/email)
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Verificar si el usuario está activo
            if not user.is_active:
                messages.error(request, 'Tu cuenta está desactivada. Contacta al administrador.')
                return render(request, 'login.html')
            
            # Verificar si el rol del usuario coincide con el rol esperado
            if user.role != expected_role:
                if expected_role == 'ADMIN':
                    messages.error(request, 'Este usuario no tiene permisos de administrador.')
                else:
                    messages.error(request, 'Por favor, use el inicio de sesión de administrador.')
                return render(request, 'login.html')
            
            # Login exitoso
            login(request, user)
            
            # Configurar duración de la sesión
            if not remember_me:
                request.session.set_expiry(0)
            else:
                request.session.set_expiry(1209600)  # 2 semanas
            
            # Obtener la URL de redirección
            next_url = request.GET.get('next')
            if next_url:
                return HttpResponseRedirect(next_url)
            
            messages.success(request, f'¡Bienvenido de nuevo, {user.get_full_name() or user.username}!')
            
            # Redirección directa según el rol
            if user.is_admin():
                return HttpResponseRedirect(reverse('login:admin_dashboard'))
            return HttpResponseRedirect(reverse('login:customer_dashboard'))
        else:
            messages.error(request, 'Usuario/email o contraseña incorrectos. Por favor, intenta de nuevo.')
    
    return render(request, 'login.html')

@csrf_protect
def register_view(request):
    if request.user.is_authenticated:
        if request.user.is_admin():
            return HttpResponseRedirect(reverse('login:admin_dashboard'))
        return HttpResponseRedirect(reverse('login:customer_dashboard'))
        
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                messages.success(request, '¡Registro exitoso! Bienvenido a Zultech.')
                
                # Redirección directa según el rol
                if user.is_admin():
                    return HttpResponseRedirect(reverse('login:admin_dashboard'))
                return HttpResponseRedirect(reverse('login:customer_dashboard'))
            except Exception as e:
                messages.error(request, f'Error al crear el usuario: {str(e)}')
        else:
            # Mostrar errores específicos del formulario
            for field, errors in form.errors.items():
                for error in errors:
                    if field == '__all__':
                        messages.error(request, error)
                    else:
                        field_label = form.fields[field].label if field in form.fields else field
                        messages.error(request, f'{field_label}: {error}')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'register.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'Has cerrado sesión exitosamente.')
    return HttpResponseRedirect(reverse('login:login'))

@login_required
def profile_view(request):
    if request.method == 'POST':
        # Actualizar campos individuales
        user = request.user
        
        # Actualizar solo los campos que se envían en el formulario
        if 'username' in request.POST and request.POST['username']:
            # Verificar si el username ya existe (excepto el actual)
            username = request.POST['username']
            if CustomUser.objects.filter(username=username).exclude(id=user.id).exists():
                messages.error(request, 'Este nombre de usuario ya está en uso.')
            else:
                user.username = username
                user.save()
                messages.success(request, 'Usuario actualizado exitosamente.')
        
        if 'first_name' in request.POST:
            user.first_name = request.POST['first_name']
            user.save()
            messages.success(request, 'Nombre actualizado exitosamente.')
        
        if 'last_name' in request.POST:
            user.last_name = request.POST['last_name']
            user.save()
            messages.success(request, 'Apellido actualizado exitosamente.')
        
        if 'Correo_Electronico' in request.POST:
            email = request.POST['Correo_Electronico']
            # Verificar si el email ya existe (excepto el actual)
            if CustomUser.objects.filter(email=email).exclude(id=user.id).exists():
                messages.error(request, 'Este email ya está en uso.')
            else:
                user.email = email
                user.Correo_Electronico = email
                user.save()
                messages.success(request, 'Email actualizado exitosamente.')
        
        if 'Telefono' in request.POST:
            user.Telefono = request.POST['Telefono']
            user.save()
            messages.success(request, 'Teléfono actualizado exitosamente.')
        
        if 'Direccion' in request.POST:
            user.Direccion = request.POST['Direccion']
            user.save()
            messages.success(request, 'Dirección actualizada exitosamente.')
        
        return HttpResponseRedirect(reverse('login:profile'))
    
    # Obtener estadísticas para el dashboard
    from app_products.models import Product
    from app_cart.models import Cart
    
    try:
        total_products = Product.objects.filter(available=True).count()
    except:
        total_products = 0
    
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.get_total_items()
    except:
        cart_items = 0
    
    context = {
        'total_products': total_products,
        'pending_orders': 0,  # TODO: Obtener de app_orders
        'cart_items': cart_items,
    }
    
    return render(request, 'profile.html', context)

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
        return HttpResponseRedirect(reverse('admin_dashboard'))
    # Datos para el dashboard de cliente
    context = {
        'total_orders': 0,  # TODO: Obtener pedidos del cliente
        'cart_items': 0,  # TODO: Obtener items en carrito
        'wishlist_items': 0  # TODO: Obtener items en lista de deseos
    }
    return render(request, 'customer/dashboard.html', context)

@login_required
def redirect_to_dashboard(request):
    if request.user.is_admin():
        return HttpResponseRedirect(reverse('login:admin_dashboard'))
    return HttpResponseRedirect(reverse('login:customer_dashboard'))

@login_required
def password_change_view(request):
    """Vista para cambiar la contraseña del usuario autenticado"""
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')
        
        user = request.user
        
        # Verificar contraseña actual
        if not user.check_password(old_password):
            messages.error(request, 'La contraseña actual es incorrecta.')
            return HttpResponseRedirect(reverse('login:profile'))
        
        # Verificar que las nuevas contraseñas coincidan
        if new_password1 != new_password2:
            messages.error(request, 'Las nuevas contraseñas no coinciden.')
            return HttpResponseRedirect(reverse('login:profile'))
        
        # Verificar longitud mínima
        if len(new_password1) < 8:
            messages.error(request, 'La contraseña debe tener al menos 8 caracteres.')
            return HttpResponseRedirect(reverse('login:profile'))
        
        # Cambiar la contraseña
        user.set_password(new_password1)
        user.save()
        
        # Mantener la sesión activa después del cambio
        from django.contrib.auth import update_session_auth_hash
        update_session_auth_hash(request, user)
        
        messages.success(request, 'Contraseña actualizada exitosamente.')
        return HttpResponseRedirect(reverse('login:profile'))
    
    return HttpResponseRedirect(reverse('login:profile'))