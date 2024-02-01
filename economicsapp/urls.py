from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='economics'),
    path('EIR', views.EIR, name='EIR'),

]