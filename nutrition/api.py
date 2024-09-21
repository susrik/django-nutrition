from typing import Iterable, List
# from django.http import HttpResponse
from django.utils import timezone
# from django import forms
from .models import Portion, Food, Meal
# from django.views import generic
# from django.template import loader
# from django.shortcuts import render, redirect


class MealTotal:
    def __init__(self, name: str, portions: Iterable[Portion]):
        self.name = name
        self.portions = portions
        self.calories = sum(p.calories() for p in portions)

    def to_dict(self):
        return {
            'name': self.name,
            'calories': self.calories,
            'portions': self.portions
        }

    @staticmethod
    def split_portions(portions: Iterable[Portion]) -> List['MealTotal']:
        _meals = dict()
        for p in portions:
            meal_name = p.meal.name if p.meal else 'other'
            _m = _meals.setdefault(meal_name, []).append(p)
        return [MealTotal(_name, _portions) for _name, _portions in _meals.items()]


class DayTotal:
    def __init__(self, date: timezone, portions: Iterable[Portion]):
        self.date = date
        self.calories = sum(p.calories() for p in portions)
        self.meals = MealTotal.split_portions(portions)

    @staticmethod
    def split_days(portions: Iterable[Portion]) -> List['DayTotal']:
        portions_per_day = dict()
        for p in portions:
            portions_per_day.setdefault(p.date, []).append(p)

        return [DayTotal(date, portions) for date, portions in portions_per_day.items()]

