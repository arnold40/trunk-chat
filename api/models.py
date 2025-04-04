from django.db import models
from django.contrib.postgres.fields import ArrayField

class UserFavFood(models.Model):
    name = models.TextField()
    fav_foods = ArrayField(models.CharField(max_length=100), blank=True, default=list)
    is_vegetarian = models.BooleanField(default=False)

    class Meta:
        db_table = 'api_userfavfood'  # Explicitly set the table name

    def save(self, *args, **kwargs):
        vegetarian_foods = {"tofu", "salad", "vegetable", "fruit", "beans", "lentils", "chickpeas", "quinoa", "tempeh", "nuts", "seeds", "mango", "ice cream", "chocolate cake"}
        non_veg_foods = {"chicken", "beef", "pork", "fish", "shrimp", "bacon", "ham", "lamb", "turkey", "steak"}

        food_items = {item.lower().strip() for item in self.fav_foods}

        if food_items.intersection(non_veg_foods):
            self.is_vegetarian = False
        elif food_items.intersection(vegetarian_foods):
            self.is_vegetarian = True
        print(self.is_vegetarian)

        super().save(*args, **kwargs)