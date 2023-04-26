from django.urls import path
from . import views

app_name = "weather"

urlpatterns = [
    path('', views.index, name='weather-index'),
    path('CNjokes/', views.CNJokes, name='cnjokes'),
]