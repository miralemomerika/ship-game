from rest_framework import status, response
from rest_framework.decorators import api_view
import requests


@api_view(['GET'])
def readiness_probe(request):
    try:
        from django.db import connection
        connection.ensure_connection()
    except Exception as e:
        return response.Response({'status': 'error', 'message': str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    
    return response.Response({'status': 'ok'}, status=status.HTTP_200_OK)

@api_view(['GET'])
def liveness_probe(request):
    try:
        liveness_response = requests.get('http://localhost:8000/api/schema/swagger-ui/')
        liveness_response.raise_for_status()
    except Exception as e:
        return response.Response({'status': 'error', 'message': str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    
    return response.Response({'status': 'ok'}, status=status.HTTP_200_OK)