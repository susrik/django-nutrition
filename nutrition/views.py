from typing import Iterable, List
from django.http import HttpResponse
from django.utils import timezone
from django import forms
from . import api, models
from django.views import generic
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse

def index(request):
  return HttpResponse('nutrition index')


class DaysView(LoginRequiredMixin, generic.ListView):
    template_name = 'nutrition/days.html'
    context_object_name = 'days'

    def get_queryset(self):
        start_date = timezone.now() - timezone.timedelta(weeks=4)
        _days = api.DayTotal.split_days(models.Portion.objects.filter(date__gte=start_date))
        return sorted(_days, key=lambda d: d.date, reverse=True)


@login_required
def day(request, day_str):
    meals = api.MealTotal.split_portions(models.Portion.objects.filter(date=day_str))
    template = loader.get_template("nutrition/day.html")
    context = {
        'meals': meals,
        'date': day_str,
        'calories': sum(m.calories for m in meals)
    }
    return HttpResponse(template.render(context, request))


class PortionForm(forms.ModelForm):
    class Meta:
        model = models.Portion
        fields = ['date', 'quantity', 'food', 'meal', 'note']
        widgets = {
            'date': forms.DateInput(attrs={
                  # DaisyUI input styling
                'class': 'input input-bordered w-full max-w-xs',
                'type': 'date'}),
            'quantity': forms.NumberInput(attrs={
                  # DaisyUI input styling
                'class': 'input input-bordered w-full max-w-xs',
                'step': 0.01}),
            'food': forms.Select(attrs={
                # DaisyUI select style
                'class': 'select select-bordered w-full max-w-xs',
            }),
            'meal': forms.Select(attrs={
                # DaisyUI select style
                'class': 'select select-bordered w-full max-w-xs',
            }),
            'note': forms.TextInput(attrs={
                # DaisyUI input styling
                'class': 'input input-bordered w-full max-w-xs',
            }),
          }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        assert user  # sanity (should always be logged in here)
        super(PortionForm, self).__init__(*args, **kwargs)
        self.fields['food'].queryset = models.Food.objects.filter(user=user)
        self.fields['meal'].queryset = models.Meal.objects.filter(user=user)


@login_required
def add_portion(request):
    default_date = request.GET.get('date', timezone.now().date())

    if request.method == 'POST':
        form = PortionForm(request.POST, user=request.user)
        if form.is_valid():
            portion_instance = form.save(commit=False)
            portion_instance.user = request.user
            portion_instance.save()

            selected_date = form.cleaned_data['date']
            day_str = selected_date.strftime('%Y-%m-%d')
            return redirect('day', day_str=day_str)
    else:
        form = PortionForm(initial={'date': default_date}, user=request.user)
    
    return render(request, 'nutrition/add_portion.html', {'form': form})


class UserPreferencesForm(forms.ModelForm):
    class Meta:
        model = models.Preferences
        fields = ['max_calories', 'theme']
        # widgets = {
        #     'max_calories': forms.NumberInput(attrs={
        #           # DaisyUI input styling
        #         'class': 'input input-bordered w-full max-w-xs',
        #         'step': 0.01}),
        #     'theme': forms.Select(attrs={
        #         # DaisyUI select style
        #         'class': 'select select-bordered w-full max-w-xs',
        #     }),
        #   }

    def __init__(self, *args, **kwargs):
        _prefs = kwargs.get('instance')
        assert isinstance(_prefs, models.Preferences)  # sanity
        super(UserPreferencesForm, self).__init__(*args, **kwargs)
        self.fields['max_calories'].initial = _prefs.max_calories


@login_required
def user_preferences(request):

    preferences, created = models.Preferences.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserPreferencesForm(request.POST, instance=preferences)
        if form.is_valid():
            form.save()
            return redirect('days')
    else:
        form = UserPreferencesForm(instance=preferences)

    return render(request, 'nutrition/user-preferences.html', {'form': form})