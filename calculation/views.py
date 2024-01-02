
from django.shortcuts import render
from django.views import View
from .forms import SalaryCalculationForm
class SalaryCalculationView(View):
    template_name = 'calculation/calculate.html'
 #can you recognize graph?
    def get(self, request):
        form = SalaryCalculationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = SalaryCalculationForm(request.POST)
        if form.is_valid():
            rank = form.cleaned_data['rank']
            overtime_hours = form.cleaned_data['overtime_hours']
            night_hours = form.cleaned_data['night_hours']
            holiday_hours = form.cleaned_data['holiday_hours']

            # 여기서 계산 로직을 추가하세요.

            return render(request, self.template_name, {'form': form, 'result': '계산 결과'})
        
        return render(request, self.template_name, {'form': form})
def calculate_salary(request):
    if request.method == 'POST':
        form = SalaryCalculationForm(request.POST)
        if form.is_valid():
            # 여기서 수당 계산 로직을 추가하세요
            rank = form.cleaned_data['rank']
            overtime_hours = form.cleaned_data['overtime_hours']
            night_hours = form.cleaned_data['night_hours']
            holiday_hours = form.cleaned_data['holiday_hours']

            # 수당 계산 로직을 적용하여 결과를 계산합니다.
            # 이 부분은 실제 수당 계산에 따라 수정이 필요합니다.
            salary_result = calculate_salary_logic(rank, overtime_hours, night_hours, holiday_hours)

            return render(request, 'calculation/result.html', {'form': form, 'salary_result': salary_result})
    else:
        form = SalaryCalculationForm()

    return render(request, 'calculation/calculate.html', {'form': form})

def calculate_salary_logic(rank, overtime_hours, night_hours, holiday_hours):
    # 실제 수당 계산 로직을 작성하세요
    # 이 부분은 예시이며, 실제 수당 계산에 따라 수정이 필요합니다.
    
    if rank == 'sun':
            
        overtime_rate = 9927  # 초과시간 수당 비율
        night_rate = 3309  # 야간시간 수당 비율
        holiday_rate = 79797
        
    if rank == 'jang':
        overtime_rate = 10820
        night_rate=3607
        holiday_rate = 86979
    if rank == 'sa':
        overtime_rate= 12133
        night_rate = 4045
        holiday_rate=97527
    
    if rank == 'wi':
        overtime_rate=12925
        night_rate = 4308
        holiday_rate= 103901
    
    if rank == 'gam':
        overtime_rate = 14148
        night_rate= 4716
        holiday_rate=113727

    total_salary = (overtime_hours * overtime_rate) + (night_hours * night_rate) + (holiday_hours * holiday_rate)
    return total_salary
