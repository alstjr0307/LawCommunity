from django.contrib import admin
from django.urls import path
from .views import RealEstateTransactionView
  
urlpatterns = [
    path('', RealEstateTransactionView.as_view(), name='real_estate_transactions'),
]