from django.shortcuts import render
from django.views.generic import TemplateView
import pandas as pd

class RealEstateTransactionView(TemplateView):
    template_name = 'realEstate/show_price.html'

    def get_context_data(self, **kwargs):
        # Load data from CSV
        df = pd.read_csv('data.csv')
        df = df[['아파트', '거래금액', '전용면적', '층']]
        # Convert data to list of dictionaries
        data = df.to_dict(orient='records')
        # Return context with data
        context = super().get_context_data(**kwargs)
        context['data'] = data
        return context