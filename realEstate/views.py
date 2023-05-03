from django.shortcuts import render
from django.views.generic import TemplateView
import pandas as pd

class RealEstateTransactionView(TemplateView):
    template_name = 'realEstate/show_price.html'

    def get_context_data(self, **kwargs):
        # Load data from CSV
        df = pd.read_csv('data.csv')
        df = df[['아파트', '거래금액', '전용면적', '층', '년','월','일','거래일자']]
        
        # Filter data by date range
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        if start_date and end_date:
            df = df.loc[(df['거래일자'] >= start_date) & (df['거래일자'] <= end_date)]
        
        # Convert data to list of dictionaries
        data = df.to_dict(orient='records')
        
        # Return context with data
        context = super().get_context_data(**kwargs)
        context['data'] = data
        return context