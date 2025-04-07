import traceback
import logging
import os
from rest_framework.views import APIView
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from concurrent.futures import ThreadPoolExecutor

from .models import User
from .services import FoodSimulationService
from .serializers import UserSerializer

# Configure logging
logger = logging.getLogger(__name__)

class UserViewSet(APIView):
    permission_classes = [IsAuthenticated]
    """API View for managing and simulating user favorite foods."""

    def get(self, request):
        print("ENV: " + str(os.getenv("ENV")))
        """Fetches all vegetarian user favorite foods."""
        try:
            users = User.objects.filter(is_vegetarian=True).prefetch_related('fav_foods')
            if not users.exists():
                total_records = User.objects.count()
                logger.info("No vegetarian user records found.")
                return JsonResponse({"message": f"No vegetarian user found in {total_records} records."},
                                    status=status.HTTP_404_NOT_FOUND)

            serializer = UserSerializer(users, many=True)
            logger.info(f"Fetched {len(serializer.data)} vegetarian user records.")
            return JsonResponse({"response": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error fetching vegetarian users: {e}")
            return JsonResponse({"error": "Failed to fetch data", "details": str(e)},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        """Simulates favorite food for a user and returns one user's response."""
        try:
            food_simulation_service = FoodSimulationService()
            user = food_simulation_service.simulate_user_fav_food()

            if not user:
                return JsonResponse({"error": "Failed to generate favorite food data."},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            serializer = UserSerializer(user)
            logger.info(f"Successfully created user with favorite food entry: {serializer.data}")
            return JsonResponse({"response": serializer.data}, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            logger.warning(f"Validation error: {e}")
            return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(f"Unexpected error in food simulation: {e}\n{traceback.format_exc()}")
            return JsonResponse({"error": "Internal Server Error", "details": str(e)},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request):
        """Creates 100 users with simulated favorite food data concurrently."""
        try:
            food_simulation_service = FoodSimulationService()

            def create_user(_):
                user = food_simulation_service.simulate_user_fav_food()
                if user:
                    return UserSerializer(user).data
                else:
                    return None

            with ThreadPoolExecutor(max_workers=10) as executor:
                results = list(executor.map(create_user, range(10)))

            # Filter out any None results (in case simulation failed for some users)
            successful_results = [result for result in results if result]

            if not successful_results:
                return JsonResponse({"error": "Failed to generate any favorite food data."},
                                     status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            logger.info(f"Successfully created {len(successful_results)} users with favorite food data.")
            return JsonResponse({"response": successful_results}, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(f"Unexpected error in bulk user creation: {e}\n{traceback.format_exc()}")
            return JsonResponse({"error": "Internal Server Error", "details": str(e)},
                                 status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request):
        """Deletes all user favorite food records."""
        User.objects.all().delete()
        logger.info("All user favorite food records deleted.")
        return JsonResponse({"message": "Database cleaned successfully."}, status=status.HTTP_200_OK)