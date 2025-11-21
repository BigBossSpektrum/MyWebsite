from django.contrib.auth import logout
from django.utils import timezone
from datetime import timedelta


class SessionTimeoutMiddleware:
    """
    Middleware que cierra la sesión del usuario después de 30 minutos de inactividad.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        # Tiempo de inactividad permitido (30 minutos)
        self.timeout = timedelta(minutes=30)
    
    def __call__(self, request):
        if request.user.is_authenticated:
            # Obtener el timestamp de la última actividad
            last_activity = request.session.get('last_activity')
            
            if last_activity:
                # Convertir string a datetime
                last_activity = timezone.datetime.fromisoformat(last_activity)
                
                # Verificar si ha pasado más tiempo del permitido
                if timezone.now() - last_activity > self.timeout:
                    # Cerrar sesión automáticamente
                    logout(request)
                    # No actualizar last_activity para forzar el cierre
                else:
                    # Actualizar el timestamp de última actividad
                    request.session['last_activity'] = timezone.now().isoformat()
            else:
                # Primera vez que se registra actividad en esta sesión
                request.session['last_activity'] = timezone.now().isoformat()
        
        response = self.get_response(request)
        return response
