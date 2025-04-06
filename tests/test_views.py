import pytest
import json
from unittest.mock import patch
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from api.models import User, UserFavFood

@pytest.mark.django_db
def test_get_vegetarian_users():
    # Create a vegetarian user for the test
    user = User.objects.create(name="Veggie User", is_vegetarian=True)
    UserFavFood.objects.create(user=user, food_name="Salad", is_veggie=True)

    client = APIClient()
    url = reverse('users')

    # Temporarily patch the permission classes
    with patch('api.views.UserViewSet.permission_classes', []):
        response = client.get(url)
        data = json.loads(response.content)

        assert response.status_code == status.HTTP_200_OK
        assert len(data['response']) == 1
        assert data['response'][0]['name'] == "Veggie User"

@pytest.mark.django_db
def test_post_simulate_food():
    client = APIClient()
    url = reverse('users')

    # Temporarily patch the permission classes
    with patch('api.views.UserViewSet.permission_classes', []):
        response = client.post(url)
        data = json.loads(response.content)

        assert response.status_code == status.HTTP_201_CREATED
        assert 'response' in data
