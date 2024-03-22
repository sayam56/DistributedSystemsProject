from django.http import HttpResponse,HttpRequest
from django.shortcuts import render

from django.template.loader import render_to_string


# Create your views here.
def homepage(request):
    return render(request, 'django_app/homepage.html')

#
# def temp1(request):
#     return render(request, 'ByteBusterApp/template1.html', )
#
#
# def temp1edit(request):
#     return render(request, 'ByteBusterApp/template1editor.html', )
#
#
# def temp2(request):
#     return render(request, 'ByteBusterApp/template2.html', )
#
#
# def temp3(request):
#     return render(request, 'ByteBusterApp/template3.html', )
#
#
# def load_template(request, template_id):
#     template_name = 'ByteBusterApp/' + template_id + '.html'
#     html = render_to_string(template_name, request=request)
#     return HttpResponse(html)

def predict(request):
    return render(request, 'django_app/predict.html')

def validate_ticker(ticker_input):
    valid_tickers=[ ]
    #tickers are all uppercase
    ticker_upper_value=ticker_input.upper()
    return ticker_upper_value in valid_tickers


import yfinance as yf
def download_data( ticker_value):
    try:
        df=yf.download(tickers=ticker_value,period='1d',interval='1m')
        print(f"{ticker_value} downloaded")
        return df
    except Exception as e:
        print(e) #Log error
        return


import numpy as np
from sklearn import preprocessing,model_selection,linear_model
from sklearn.linear_model import LinearRegression
import plotly.graph_objects as go
from plotly.offline import plot
import datetime as dt
def perform_prediction(ticker_value,df,input_days):
    #ML prediction code here
    fig = go.Figure(data=[
        go.Line(x=df['Date'], y=df['StockPrice'])  # Replace 'Date' and 'StockPrice' with your actual DataFrame columns
    ])
    plot_div = plot(fig, output_type='div', include_plotlyjs=False)
    #After preparing preddiction and plot
    context={
        'plot_div':plot_div,
    }
    return context

import pandas as pd
def get_ticker_info(ticker_value, csv_path='/path/to/ticker_info.csv'):
    df = pd.read_csv(csv_path)
    ticker_info_row = df[df['Ticker'] == ticker_value]
    if not ticker_info_row.empty:
        ticker_info = ticker_info_row.to_dict('records')[0]
    else:
        ticker_info = {"error": "Ticker not found"}
    return ticker_info

def stock_prediction_view(request):
    if request.method == "POST":
        ticker_input = request.POST.get("ticker", "").strip()
        #input_days = request.POST.get("days", "10").strip()

        # Validate the ticker
        # Assuming validate_ticker is adjusted to return a boolean or similar instead of HttpResponse
        if not validate_ticker(request, ticker_input):
            return render(request, 'Ticker_Unfounded.html')

        # Download data
        df=download_data(ticker_input)
        if df is None:
            return render(request,'yf_error.html')
        # Input days validation
        try:
            input_days=int(request.POST.get('days',10))
            if input_days<0:
                raise ValueError("Input days cannot be less than zero.")
            elif input_days>365:
                raise ValueError("Input days cannot be greater than 365")

        except ValueError as e:
            context = {'error': str(e)}
            return render(request, 'Input_Days_Error.html', context)


        # Step 4: Perform prediction and generate the plot
        context = perform_prediction( ticker_input, df, input_days)
        ticker_info=get_ticker_info(ticker_input)
        context.update({'ticker_info':ticker_info})
        return render(request, "predict.html", context)

    # GET request or initial page load
    return render(request, "stock_input_form.html")
