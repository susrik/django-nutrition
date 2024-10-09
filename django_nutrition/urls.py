from django.urls import path
from django.contrib.auth import views as auth_views

from . import views, api

urlpatterns = [
    path("", views.DaysView.as_view(), name="days"),
    path("foods", views.FoodsView.as_view(), name="foods"),
    path("day/<str:day_str>", views.day, name="day"),
    path("user-preferences/", views.user_preferences, name="user_preferences"),
    path("api/events/", api.days, name="day-events"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="django_nutrition/login.html"),
        name="nutrition_login",
    ),
    path("style-test/", views.style_test, name="style_test"),
    path("portion/new", views.add_or_edit_portion, name="add_or_edit_portion"),
    path(
        "portion/edit/<int:pk>/", views.add_or_edit_portion, name="add_or_edit_portion"
    ),
    path("portion/delete/<int:pk>/", views.delete_portion, name="delete_portion"),
    path("food/new", views.add_or_edit_food, name="add_or_edit_food"),
    path("food/edit/<int:pk>/", views.add_or_edit_food, name="add_or_edit_food"),
    # path('food/delete/<int:pk>/', views.delete_food, name='delete_food'),
]
