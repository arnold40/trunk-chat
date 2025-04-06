import pytest
from unittest.mock import patch
from api.models import User, UserFavFood
from api.services import FoodSimulationService

@pytest.mark.django_db
@patch('api.services.GPTClient.ask_question')
def test_generate_fav_foods_returns_parsed_data(mock_ask):
    mock_ask.side_effect = [
        "What are your top 3 favorite foods?",
        '{"foods": [{"name": "Pizza", "is_veggie": true}, {"name": "Curry", "is_veggie": true}]}'
    ]

    service = FoodSimulationService()
    foods = service.generate_fav_foods()

    assert foods is not None
    assert isinstance(foods, list)
    assert foods[0]["name"] == "Pizza"

@pytest.mark.django_db
@patch('api.services.FoodSimulationService.generate_fav_foods')
def test_simulate_user_fav_food_creates_user_and_foods(mock_generate):
    mock_generate.return_value = [
        {"name": "Sushi", "is_veggie": False},
        {"name": "Salad", "is_veggie": True},
        {"name": "Curry", "is_veggie": True},
    ]

    service = FoodSimulationService()
    user = service.simulate_user_fav_food()

    assert user is not None
    assert User.objects.count() == 1
    assert UserFavFood.objects.count() == 3
    assert user.fav_foods.count() == 3
