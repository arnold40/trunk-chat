import traceback
import logging
from rest_framework.views import APIView
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from rest_framework import status

from .models import UserFavFood
from .services import FoodSimulationService
from .serializers import UserFavFoodSerializer

# Configure logging
logger = logging.getLogger(__name__)

class UserViewSet(APIView):
    """API View for managing and simulating user favorite foods."""

    def get(self, request):
        """Fetches all vegetarian user favorite foods."""
        try:
            users_fav_food = UserFavFood.objects.filter(is_vegetarian=True)
            serializer = UserFavFoodSerializer(users_fav_food, many=True)
            logger.info(f"Fetched {len(serializer.data)} vegetarian user favorite food records.")
            return JsonResponse({"response": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({"error": "Failed to fetch data", "details": str(e)},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        """Simulates favorite food for a user and returns one user's response."""
        try:
            food_simulation_service = FoodSimulationService()
            user_fav_food = food_simulation_service.simulate_user_fav_food()

            if not user_fav_food:
                return JsonResponse({"error": "Failed to generate favorite food data."},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            serializer = UserFavFoodSerializer(user_fav_food)
            logger.info(f"Successfully created favorite food entry: {serializer.data}")
            return JsonResponse({"response": serializer.data}, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            logger.warning(f"Validation error: {e}")
            return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(f"Unexpected error in food simulation: {e}\n{traceback.format_exc()}")
            return JsonResponse({"error": "Internal Server Error", "details": str(e)},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request):
        """Deletes all user favorite food records."""
        UserFavFood.objects.all().delete()
        logger.info("All user favorite food records deleted.")
        return JsonResponse({"message": "Database cleaned successfully."}, status=status.HTTP_200_OK)