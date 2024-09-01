from django.db import models
from django.utils import timezone


class Food(models.Model):
    name = models.CharField(max_length=200)
    calories = models.FloatField()


class Meal(models.Model):
    name = models.CharField(max_length=200)


class Portion(models.Model):
    date = models.DateField(default=timezone.now().date())
    quantity = models.IntegerField(default=1)
    note = models.CharField(max_length=200, blank=True)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, blank=True)
