from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.
def Dashboard(request):
    return render(request, 'home.html')

def contact(request):
    return render(request, 'contact.html')

def privacy_policy(request):
    return render(request, 'privacy_policy.html')

def data_deletion(request):
    return render(request, 'data_deletion.html')

@csrf_exempt
def facebook_data_deletion_callback(request):
    """Endpoint para el callback de eliminación de datos de Facebook"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            signed_request = data.get('signed_request', '')
            
            # Aquí procesarías la solicitud de eliminación
            # Por ahora solo retornamos una confirmación
            
            confirmation_code = f"deletion_{signed_request[:10]}"
            
            return JsonResponse({
                'url': f'http://localhost:8000/data-deletion/?confirmation={confirmation_code}',
                'confirmation_code': confirmation_code
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    # Si es GET, mostrar la página de instrucciones
    return render(request, 'data_deletion.html')

