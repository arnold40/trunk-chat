import pytest

from api.models import User, UserFavFood


@pytest.mark.django_db
def test_user_becomes_vegetarian_when_all_foods_are_veggie():
    user = User.objects.create(name="Alice")
    UserFavFood.objects.create(user=user, food_name="Tofu", is_veggie=True)
    UserFavFood.objects.create(user=user, food_name="Broccoli", is_veggie=True)
    UserFavFood.objects.create(user=user, food_name="Salad", is_veggie=True)

    user.refresh_from_db()
    assert user.is_vegetarian is True

@pytest.mark.django_db
def test_user_not_vegetarian_if_any_food_is_not_veggie():
    user = User.objects.create(name="Bob")
    UserFavFood.objects.create(user=user, food_name="Steak", is_veggie=False)
    UserFavFood.objects.create(user=user, food_name="Salad", is_veggie=True)
    UserFavFood.objects.create(user=user, food_name="Broccoli", is_veggie=True)

    user.refresh_from_db()
    assert user.is_vegetarian is False
