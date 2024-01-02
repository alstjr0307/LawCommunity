# urls.py
from django.urls import path
from .views import SalaryCalculationView

app_name = 'salary'

urlpatterns = [
    path('calculate_salary/', SalaryCalculationView.as_view(), name='calculate_salary'),
    # 다른 URL 패턴들을 추가할 수 있습니다.
]
