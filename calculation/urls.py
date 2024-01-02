
from django.contrib import admin
from django.urls import path
from django.urls import path
from .views import calculate_salary
app_name = 'calculation'
urlpatterns = [
    path('', calculate_salary, name='calculate_salary'),
]