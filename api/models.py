from django.db import models

class User(models.Model):
    name = models.TextField()
    is_vegetarian = models.BooleanField(default=False)

class UserFavFood(models.Model):
    user = models.ForeignKey(User, related_name='fav_foods', on_delete=models.CASCADE)
    food_name = models.CharField(max_length=100)
    is_veggie = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the current food first

        # After saving, check all fav_foods of the user
        all_veggie = self.user.fav_foods.all().exists() and self.user.fav_foods.filter(is_veggie=False).count() == 0

        if self.user.is_vegetarian != all_veggie:
            self.user.is_vegetarian = all_veggie
            self.user.save(update_fields=['is_vegetarian'])