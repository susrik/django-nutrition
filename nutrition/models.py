from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Food(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    calories = models.FloatField()

    def __str__(self):
        return self.name


class Meal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Portion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    quantity = models.FloatField(default=1)
    note = models.CharField(max_length=200, blank=True)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    meal = models.ForeignKey(Meal, on_delete=models.SET_NULL, null=True, blank=True)

    def calories(self):
        return self.food.calories * self.quantity

    def __str__(self):
        return f'{self.food.name} ({self.quantity})'


class Preferences(models.Model):
    DEFAULT_MAX_CALORIES = 2000
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    max_calories = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f'{self.user}, max calories: {self.max_calories}'
