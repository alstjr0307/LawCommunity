# views.py
from django.shortcuts import render
from django.views import View
from .models import PoliceSalary
from .forms import SalaryCalculationForm

class SalaryCalculationView(View):
    
    template_name = 'salary/calculate.html'

    def get(self, request, *args, **kwargs):
        form = SalaryCalculationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = SalaryCalculationForm(request.POST)
        if form.is_valid():
            grade = form.cleaned_data['grade']
            rank = form.cleaned_data['rank']
            average_overtime = form.cleaned_data['average_overtime']
        
            try:
                salary_info = PoliceSalary.objects.get(grade=grade, rank=rank)
                basic_salary = salary_info.basic_salary
            except PoliceSalary.DoesNotExist:
                basic_salary = 0

            # 여기에 추가로 수당 등을 계산하는 로직을 작성

            final_salary = basic_salary 

            return render(request, 'salary/result.html', {'final_salary': final_salary})

        return render(request, self.template_name, {'form': form})
