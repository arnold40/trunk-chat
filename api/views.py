from rest_framework.views import APIView
from rest_framework.response import Response

class UserViewSet(APIView):
    """API View for managing and simulating user favorite foods."""
    def get(self, request):
        return Response({"status": "ok", "message": "ALL VEGES ARE REALLY FOR YOU!"})
