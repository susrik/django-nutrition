from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Portion, Food
from .api import MealTotal


class MealTotalTests(TestCase):
    def test_split_portions(self):
        user = User.objects.create_user("test2", "1234")

        food_100 = Food.objects.create(name="food 100", calories=100, user=user)
        Portion.objects.create(
            food=food_100, quantity=1.0, date=timezone.now(), user=user
        )

        food_200 = Food.objects.create(name="food 200", calories=200, user=user)
        Portion.objects.create(
            food=food_200, quantity=1.0, date=timezone.now(), user=user
        )

        food_300 = Food.objects.create(name="food 300", calories=300, user=user)
        Portion.objects.create(
            food=food_300, quantity=1.0, date=timezone.now(), user=user
        )

        portions = Portion.objects.all()

        meals = MealTotal.split_portions(portions)
        self.assertEqual(len(meals), 1)
        self.assertEqual(meals[0].calories, 600)


class ViewsTest(TestCase):
    USERNAME = "testuser"
    PASSWORD = "testpassword"

    def setUp(self):
        _user = User.objects.create_user(
            username=ViewsTest.USERNAME, password=ViewsTest.PASSWORD
        )

        foods = [
            Food.objects.create(name="food 100", calories=100, user=_user),
            Food.objects.create(name="food 200", calories=200, user=_user),
            Food.objects.create(name="food 300", calories=300, user=_user),
            Food.objects.create(name="food 1000", calories=1000, user=_user),
        ]

        _today = [
            Portion.objects.create(
                food=_f, quantity=1.0, date=timezone.now(), user=_user
            )
            for _f in foods
        ]

        _yesterday = [
            Portion.objects.create(
                food=_f,
                quantity=1.0,
                date=timezone.now() - timezone.timedelta(days=1),
                user=_user,
            )
            for _f in foods
        ]

        _tomorrow = [
            Portion.objects.create(
                food=_f,
                quantity=1.0,
                date=timezone.now() + timezone.timedelta(days=1),
                user=_user,
            )
            for _f in foods
        ]

    def test_add_to_cart(self):
        response = self.client.get(reverse("days"))
        # expect to be redirected to login
        self.assertEqual(response.status_code, 302)

        self.client.login(username=ViewsTest.USERNAME, password=ViewsTest.PASSWORD)
        response = self.client.get(reverse("days"))
        self.assertEqual(response.status_code, 200)
        # dumb ... should do a better test than this (e.g. dates)
        self.assertContains(response, "Calories")

    def test_days_list_api(self):
        response = self.client.get(reverse("day-events"))
        self.assertEqual(response.status_code, 403)

        self.client.login(username=ViewsTest.USERNAME, password=ViewsTest.PASSWORD)
        response = self.client.get(reverse("day-events"))
        self.assertEqual(response.status_code, 200)
        days_list = response.json()
        # very stupid hard-coded based on test setup data
        assert len(days_list) == 2
