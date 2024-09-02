from typing import Iterable, List
from django.http import HttpResponse
from django.utils import timezone
from .models import Portion, Food, Meal
from django.views import generic


class DayTotal:
    def __init__(self, date: timezone, portions: Iterable[Portion]):
        self.date = date
        self.calories = 0
        for p in portions:
            self.calories += p.food.calories * p.quantity

    @staticmethod
    def get_totals(portions: Iterable[Portion]) -> List['DayTotal']:
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
        _days = DayTotal.get_totals(Portion.objects.filter(date__gte=start_date))
        return sorted(_days, key=lambda d: d.date, reverse=True)
