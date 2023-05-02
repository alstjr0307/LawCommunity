from django.shortcuts import render
from django.views.generic import TemplateView
import pandas as pd

class RealEstateTransactionView(TemplateView):
    template_name = 'realEstate/show_price.html'

    def get_context_data(self, **kwargs):
        # 데이터를 가져와 pandas DataFrame 객체로 변환
        
        df = pd.read_csv('data.csv')
        
        # 템플릿 렌더링에 사용할 context 반환
        context = super().get_context_data(**kwargs)
        context['pandas_data'] = df.to_html()
        return context