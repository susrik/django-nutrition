import datetime

from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User

from .models import Portion, Food
from .api import MealTotal


class MealTotalTests(TestCase):

    def __str__(self):
        user = User.objects.create_user('test', '123')

        food_100 = Food.objects.create(name='food 100', calories=100, user=user)
        Portion.objects.create(food=food_100, quantity=1.0, date=timezone.now(), user=user)

        food_200 = Food.objects.create(name='food 200', calories=200, user=user)
        Portion.objects.create(food=food_200, quantity=1.0, date=timezone.now(), user=user)

        food_300 = Food.objects.create(name='food 300', calories=200, user=user)
        Portion.objects.create(food=food_300, quantity=1.0, date=timezone.now(), user=user)

        portions = Portion.objects.all()

        meal = MealTotal('test', portions)
        # self.assertEqual(meal.calories, 600)

    def test_split_portions(self):
        user = User.objects.create_user('test2', '1234')

        food_100 = Food.objects.create(name='food 100', calories=100, user=user)
        Portion.objects.create(food=food_100, quantity=1.0, date=timezone.now(), user=user)

        food_200 = Food.objects.create(name='food 200', calories=200, user=user)
        Portion.objects.create(food=food_200, quantity=1.0, date=timezone.now(), user=user)

        food_300 = Food.objects.create(name='food 300', calories=200, user=user)
        Portion.objects.create(food=food_300, quantity=1.0, date=timezone.now(), user=user)

        portions = Portion.objects.all()

        # meals = MealTotal.split_portions(portions)
        # self.assertEqual(len(meals), 1)
        # self.assertEqual(meals[0].calories, 600)
