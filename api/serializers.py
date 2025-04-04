from rest_framework import serializers
from .models import UserFavFood

class UserFavFoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFavFood
        fields = ["name", "fav_foods"]