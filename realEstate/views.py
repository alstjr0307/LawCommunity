from django.shortcuts import render
from django.views.generic import TemplateView
import pandas as pd
from .utils import m2_to_pyung, add_pyung_unit


class RealEstateTransactionView(TemplateView):
    template_name = 'realEstate/show_price.html'

    def get_context_data(self, **kwargs):
        # Load data from CSV
        df = pd.read_csv('data.csv')
        df = df[['아파트', '거래금액', '전용면적', '층', '거래일자']]
        
        # Filter data by start_date and end_date if they exist
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        if start_date and end_date:
            df = df.loc[(df['거래일자'] >= start_date) & (df['거래일자'] <= end_date)]
        
        # Filter data by apartment name if it exists
        apartment_name = self.request.GET.get('apartment_name')
        if apartment_name:
            df = df.loc[df['아파트'].str.contains(apartment_name)]

        # Convert 전용면적 column to 평 단위
        convert_to_pyung = self.request.GET.get('pyung')
        if convert_to_pyung:
            df['전용면적'] = df['전용면적'].apply(m2_to_pyung).apply(add_pyung_unit)

        # Convert data to list of dictionaries
        data = df.to_dict(orient='records')
        
        # Return context with data
        context = super().get_context_data(**kwargs)
        context['data'] = data
        return context
