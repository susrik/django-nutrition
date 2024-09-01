from django.db import models
from django.utils import timezone


class Food(models.Model):
    name = models.CharField(max_length=200)
    calories = models.FloatField()

    def __str__(self):
        return self.name


class Meal(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Portion(models.Model):
    date = models.DateField(default=timezone.now().date())
    quantity = models.FloatField(default=1)
    note = models.CharField(max_length=200, blank=True)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return f'{self.food.name} ({self.quantity})'
