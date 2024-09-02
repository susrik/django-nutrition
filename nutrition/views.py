from typing import Iterable, List
from django.http import HttpResponse
from django.utils import timezone
from .models import Portion, Food, Meal
from django.views import generic
from django.template import loader


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


def index(request):
  return HttpResponse('nutrition index')


class DaysView(generic.ListView):
    template_name = 'nutrition/days.html'
    context_object_name = 'days'

    def get_queryset(self):
        start_date = timezone.now() - timezone.timedelta(weeks=4)
        _days = DayTotal.split_days(Portion.objects.filter(date__gte=start_date))
        return sorted(_days, key=lambda d: d.date, reverse=True)


def day(request, day_str):
    meals = MealTotal.split_portions(Portion.objects.filter(date=day_str))
    template = loader.get_template("nutrition/day.html")
    context = {
        'meals': meals,
        'date': day_str,
        'calories': sum(m.calories for m in meals)
    }
    return HttpResponse(template.render(context, request))
