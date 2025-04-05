from rest_framework import serializers
from .models import User, UserFavFood

class UserFavFoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFavFood
        fields = ["food_name", "is_veggie"]

class UserSerializer(serializers.ModelSerializer):
    fav_foods = UserFavFoodSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ["name", "is_vegetarian", "fav_foods"]