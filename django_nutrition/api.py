from enum import Enum
from functools import partial
from datetime import datetime
from typing import Iterable, List, TYPE_CHECKING
from django.utils import timezone
from . import models
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import serializers

if TYPE_CHECKING:
    from django.http import HttpRequest

CALORIES_WARNING_THRESHOLD = 0.1  # cutoff for "slightly over"


def round_01(value: float) -> float:
    v10 = value * 10
    return int(v10 + 0.5) / 10


class DailyTotalRange(Enum):
    UNDER = "under"
    OVER = "over"
    SLIGHTLY_OVER = "slightly_over"


class MealTotal:
    def __init__(self, name: str, portions: Iterable[models.Portion]):
        self.name = name
        self.portions = portions
        self.calories = round_01(sum(p.calories() for p in portions))

    def to_dict(self):
        return {"name": self.name, "calories": self.calories, "portions": self.portions}

    @staticmethod
    def split_portions(portions: Iterable[models.Portion]) -> List["MealTotal"]:
        _meals = dict()
        for p in portions:
            meal_name = p.meal.name if p.meal else "other"
            _m = _meals.setdefault(meal_name, []).append(p)
        return [MealTotal(_name, _portions) for _name, _portions in _meals.items()]


class DayTotal:
    def __init__(self, date: timezone, portions: Iterable[models.Portion]):
        self.date = date
        self.calories = sum(p.calories() for p in portions)
        self.meals = MealTotal.split_portions(portions)

    @staticmethod
    def split_days(portions: Iterable[models.Portion]) -> List["DayTotal"]:
        portions_per_day = dict()
        for p in portions:
            portions_per_day.setdefault(p.date, []).append(p)

        return [DayTotal(date, portions) for date, portions in portions_per_day.items()]


class FullDayEvent:
    CALORIE_RANGE_STYLES = {
        DailyTotalRange.UNDER: {
            "backgroundColor": "green",
            "textColor": "white",
        },
        DailyTotalRange.OVER: {
            "backgroundColor": "red",
            "textColor": "white",
        },
        DailyTotalRange.SLIGHTLY_OVER: {
            "backgroundColor": "orange",
            "textColor": "black",
        },
    }

    @staticmethod
    def get_calorie_range(
        calories: float, max_calories: float, warning_threshold: float = 0
    ) -> DailyTotalRange:
        assert warning_threshold > 0
        if calories < max_calories:
            return DailyTotalRange.UNDER
        elif calories > max_calories * (1 + CALORIES_WARNING_THRESHOLD):
            return DailyTotalRange.OVER
        else:
            return DailyTotalRange.SLIGHTLY_OVER

    def __init__(
        self, day: DayTotal, max_calories: float, warning_threshold: float = 0
    ):
        self.title = str(int(day.calories + 0.5))
        self.start = day.date
        self.end = day.date
        self.allDay = True
        self.description = f"{day.calories} calories"
        # self.display = 'background'
        self.display = "auto"
        self.url = f"/nutrition/day/{day.date}"

        range = self.get_calorie_range(day.calories, max_calories, warning_threshold)
        style = FullDayEvent.CALORIE_RANGE_STYLES[range]
        self.backgroundColor = style["backgroundColor"]
        self.textColor = style["textColor"]


class FullDayEventSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    start = serializers.DateField()
    end = serializers.DateField()
    description = serializers.CharField(max_length=200)
    allDay = serializers.BooleanField()
    display = serializers.CharField(max_length=200)
    backgroundColor = serializers.CharField(max_length=200)
    textColor = serializers.CharField(max_length=200)
    url = serializers.CharField(max_length=200)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def days(request: "HttpRequest"):
    start = request.query_params.get("start", None)
    if start:
        # FullCalendar doesn't send timezone info
        start_date = datetime.fromisoformat(start)
    else:
        start_date = timezone.now() - timezone.timedelta(weeks=4)

    end = request.query_params.get("end", None)
    if end:
        # FullCalendar doesn't send timezone info
        end_date = datetime.fromisoformat(end)
    else:
        end_date = timezone.now()

    _days = DayTotal.split_days(
        models.Portion.objects.filter(
            date__gte=start_date, date__lte=end_date, user=request.user
        )
    )

    _prefs = models.Preferences.current_preferences(request)

    _make_event = partial(
        FullDayEvent,
        max_calories=_prefs["max_calories"],
        warning_threshold=CALORIES_WARNING_THRESHOLD,
    )
    serializer = FullDayEventSerializer(map(_make_event, _days), many=True)
    return Response(serializer.data)
