from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Portion, Food, Meal
from .api import MealTotal
from datetime import timedelta

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


class AddOrEditPortionViewTest(TestCase):
    USERNAME = "testuser"
    PASSWORD = "12345"

    def setUp(self):
        self.user = User.objects.create_user(
            username=AddOrEditPortionViewTest.USERNAME,
            password=AddOrEditPortionViewTest.PASSWORD)
        self.food = Food.objects.create(
            name='Test Food', calories=100, user=self.user)
        self.meal = Meal.objects.create(
            name='Test Meal', user=self.user)

    def test_edit_portion_default_date(self):
        # Create a portion from a week ago
        one_week_ago = timezone.now().date() - timedelta(days=7)
        portion = Portion.objects.create(
            user=self.user,
            food=self.food,
            meal=self.meal,
            quantity=1,
            date=one_week_ago
        )

        # Log in the user
        self.client.login(
            username=AddOrEditPortionViewTest.USERNAME,
            password=AddOrEditPortionViewTest.PASSWORD)

        # Get the edit portion page
        response = self.client.get(reverse(
            'add_or_edit_portion', kwargs={'pk': portion.pk}
        ))

        # Check that the response is successful
        self.assertEqual(response.status_code, 200)

        # Check that the default date in the form is correct
        self.assertContains(response, f'value="{one_week_ago.isoformat()}"')

        # Optionally, you can also check the form's initial data
        form = response.context['form']
        self.assertEqual(form.initial['date'], one_week_ago)
