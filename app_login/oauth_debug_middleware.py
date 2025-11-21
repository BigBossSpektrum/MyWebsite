"""
Middleware para debugging de OAuth
"""
import traceback

class OAuthDebugMiddleware:
    """Middleware para capturar y mostrar errores de OAuth"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        return response
    
    def process_exception(self, request, exception):
        """Capturar excepciones durante OAuth"""
        return None
