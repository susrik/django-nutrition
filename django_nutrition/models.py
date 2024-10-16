from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.http import HttpRequest


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

    def calories_rounded_01(self):
        c10 = self.calories() * 10
        return int(c10 + 0.5) / 10

    def __str__(self):
        return f"{self.food.name} ({self.quantity})"


class Preferences(models.Model):
    DEFAULT_MAX_CALORIES = 2000
    DEFAULT_THEME = "light"

    AVAILABLE_THEMES = [
        "light",
        "dark",
        "cupcake",
        "bumblebee",
        "emerald",
        "corporate",
        "synthwave",
        "retro",
        "cyberpunk",
        "valentine",
        "halloween",
        "garden",
        "forest",
        "aqua",
        "lofi",
        "pastel",
        "fantasy",
        "wireframe",
        "black",
        "luxury",
        "dracula",
        "cmyk",
        "autumn",
        "business",
        "acid",
        "lemonade",
        "night",
        "coffee",
        "winter",
        "dim",
        "nord",
        "sunset",
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    max_calories = models.FloatField(blank=True, null=True)
    theme = models.CharField(
        max_length=200,
        choices=[(t, t) for t in AVAILABLE_THEMES],
        blank=True,
        null=True,
    )

    def __str__(self):
        return f'{self.user}, max calories: {self.max_calories}, theme: "{self.theme}"'

    @staticmethod
    def current_preferences(request: "HttpRequest") -> dict:
        return_value = {
            "max_calories": Preferences.DEFAULT_MAX_CALORIES,
            "theme": Preferences.DEFAULT_THEME,
        }
        if request.user.is_authenticated:
            try:
                _prefs = Preferences.objects.get(user=request.user)
                return_value["max_calories"] = (
                    _prefs.max_calories or Preferences.DEFAULT_MAX_CALORIES
                )
                return_value["theme"] = _prefs.theme or Preferences.DEFAULT_THEME
            except Preferences.DoesNotExist:
                pass  # ok (prefs are optional)

        return return_value
