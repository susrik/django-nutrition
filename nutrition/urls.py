from django.urls import path

from . import views, api

urlpatterns = [
  path('', views.DaysView.as_view(), name='days'),
  path('day/<str:day_str>', views.day, name='day'),
  path('add-portion/', views.add_portion, name='add_portion'),
  path('api/events/', api.days, name='day-events'),
]
