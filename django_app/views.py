from django.http import HttpResponse
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

def validate_ticker(request,ticker_input):
    valid_tickers=[ ]
    #tickers are all uppercase
    ticker_upper_value=ticker_input.upper()
    if ticker_upper_value not in valid_tickers:
        return render(request,'Ticker_Unfounded.html')
    else:
        # If valid, proceed to download data
        return download_data(request, ticker_upper_value)


import yfinance as yf
def download_data(request, ticker_value):
    try:
        df=yf.download(tickers=ticker_value,period='1d',interval='1m')
        print(f"{ticker_value} downloaded")
        #proceed to prepare for prediction
        return prepare_prediction(request,ticker_value,df)
    except Exception as e:
        print(e) #Log error
        return render(request,'yf_error.html')


import numpy as np
from sklearn import preprocessing,model_selection,linear_model
def prepare_prediction(request,ticker_value,df):
    try:
        input_days=int(request.POST.get('days',10))#Default to 10
        if input_days<0:
            return render(request,'Input_Days_Less_Than_Zero.html')
        elif input_days>365:
            return render(request,'Input_Days_Greater_Than_365.html')
        else:
            return perform_prediction(request, ticker_value, df, input_days)
    except ValueError:
        return render(request, 'Input_Days_Error.html', {})

def perform_prediction():
    return