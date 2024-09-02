from django.urls import path

from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('days/', views.DaysView.as_view(), name='days'),
  path('day/<str:day_str>', views.day, name='day'),
]
