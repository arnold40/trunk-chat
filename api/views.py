from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def vegetarian_users(request):
    return Response({"status": "ok", "message": "ALL VEGES ARE REALLY FOR YOU!!!"})