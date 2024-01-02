# salary/forms.py
from django import forms

class SalaryCalculationForm(forms.Form):
    RANK_CHOICES = [
        ('sun', '순경'),
        ('jang', '경장'),
        ('sa', '경사'),
        ('wi', '경위'),
        ('gam', '경감'),
        
    ]
    STEP_CHOICES = [(str(i), f'{i}호봉') for i in range(1, 31)]  # 1부터 30까지의 호봉을 추가합니다.

    grade = forms.ChoiceField(label='계급', choices=RANK_CHOICES)
    rank = forms.ChoiceField(label='호봉', choices=STEP_CHOICES)
    average_overtime = forms.FloatField(label='평균초과시간', min_value=0.0)
