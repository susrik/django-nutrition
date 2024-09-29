from django.urls import path
from django.contrib.auth import views as auth_views

from . import views, api

urlpatterns = [
  path('', views.DaysView.as_view(), name='days'),
  path('day/<str:day_str>', views.day, name='day'),
  path('add-portion/', views.add_portion, name='add_portion'),
  path('user-preferences/', views.user_preferences, name='user_preferences'),
  path('api/events/', api.days, name='day-events'),
  path('login/', auth_views.LoginView.as_view(template_name='nutrition/login.html'), name='nutrition_login'),
  path('style-test/',views.style_test, name='style_test'),
]
