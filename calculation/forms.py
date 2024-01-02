# myapp/forms.py

from django import forms


class SalaryCalculationForm(forms.Form):
    RANK_CHOICES = [
        ('sun', '순경'),
        ('jang', '경장'),
        ('sa', '경사'),
        ('wi', '경위'),
        ('gam', '경감'),
    ]

    rank = forms.ChoiceField(choices=RANK_CHOICES, label='계급')
    overtime_hours = forms.IntegerField(label='시간외 시간')
    night_hours = forms.IntegerField(label='야간 시간')
    holiday_hours = forms.IntegerField(label='휴일')