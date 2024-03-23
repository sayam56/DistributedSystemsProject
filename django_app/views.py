from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from urllib import request
from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from django.views import View, generic
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import SignupForm
from .utils import get_news
from django.contrib.auth import authenticate, login, logout


from plotly.offline import plot
import plotly.graph_objects as go
import plotly.express as px
from plotly.graph_objs import Scatter

import pandas as pd
import numpy as np
import json

import yfinance as yf
import datetime as dt


# Create your views here.

# Dashboard when Server loads
def dashboard(request):
    # ================================================= Left Card Plot =========================================================
    # Here we used yf.download function
    data = yf.download(
        # passes the ticker
        tickers=['AAPL', 'AMZN', 'QCOM', 'META', 'NVDA', 'JPM'],

        group_by='ticker',

        threads=True,  # Set thread value to true

        # used for access data[ticker]
        period='1mo',
        interval='1d'

    )

    data.reset_index(level=0, inplace=True)

    fig_left = go.Figure()
    fig_left.add_trace(
        go.Scatter(x=data['Date'], y=data['AAPL']['Adj Close'], name="AAPL")
    )
    fig_left.add_trace(
        go.Scatter(x=data['Date'], y=data['AMZN']['Adj Close'], name="AMZN")
    )
    fig_left.add_trace(
        go.Scatter(x=data['Date'], y=data['QCOM']['Adj Close'], name="QCOM")
    )
    fig_left.add_trace(
        go.Scatter(x=data['Date'], y=data['META']['Adj Close'], name="META")
    )
    fig_left.add_trace(
        go.Scatter(x=data['Date'], y=data['NVDA']['Adj Close'], name="NVDA")
    )
    fig_left.add_trace(
        go.Scatter(x=data['Date'], y=data['JPM']['Adj Close'], name="JPM")
    )
    fig_left.update_layout(paper_bgcolor="#14151b", plot_bgcolor="#14151b", font_color="white")

    plot_div_left = plot(fig_left, auto_open=False, output_type='div')

    # ================================================ To show recent stocks ==============================================

    df1 = yf.download(tickers='AAPL', period='1d', interval='1d')
    df2 = yf.download(tickers='AMZN', period='1d', interval='1d')
    df3 = yf.download(tickers='GOOGL', period='1d', interval='1d')
    df4 = yf.download(tickers='UBER', period='1d', interval='1d')
    df5 = yf.download(tickers='TSLA', period='1d', interval='1d')
    # df6 = yf.download(tickers='TWTR', period='1d', interval='1d')

    df1.insert(0, "Ticker", "AAPL")
    df2.insert(0, "Ticker", "AMZN")
    df3.insert(0, "Ticker", "GOOGL")
    df4.insert(0, "Ticker", "UBER")
    df5.insert(0, "Ticker", "TSLA")
    # df6.insert(0, "Ticker", "TWTR")

    df = pd.concat([df1, df2, df3, df4, df5], axis=0)
    df.reset_index(level=0, inplace=True)
    df.columns = ['Date', 'Ticker', 'Open', 'High', 'Low', 'Close', 'Adj_Close', 'Volume']
    convert_dict = {'Date': object}
    df = df.astype(convert_dict)
    df.drop('Date', axis=1, inplace=True)

    json_records = df.reset_index().to_json(orient='records')
    recent_stocks = []
    recent_stocks = json.loads(json_records)

    # ========================================== Page Render section =====================================================

    return render(request, 'django_app/dashboard.html', {
        'plot_div_left': plot_div_left,
        'recent_stocks': recent_stocks
    })


def predict(request):
    response = HttpResponse()
    heading1 = '<p>' + 'PREDICT PAGE:' + '</p>'
    response.write(heading1)

    return response


def stockInfo(request):
    response = HttpResponse()
    heading1 = '<p>' + 'Stock INFo PAGE:' + '</p>'
    response.write(heading1)

    return response


def news(request):
    response = HttpResponse()
    heading1 = '<p>' + 'NEWS PAGE:' + '</p>'
    response.write(heading1)

    return response


class SignUpView(generic.CreateView):
    form_class = SignupForm
    success_url = reverse_lazy('django_app/login')  # After signing up, redirect to login page
    template_name = 'django_app/registration/signup.html'


def login_here(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('django_app:dashboard'))
            else:
                return HttpResponse('Your account is disabled')
        else:
            return HttpResponse('Login details are incorrect')
    else:
        return render(request, 'django_app/registration/login.html')


@login_required
def logout_here(request):
    logout(request)
    return HttpResponseRedirect(reverse('django_app:dashboard'))


# ========================================== News API Section =====================================================
def news_list(request):
    news_data = get_news()
    return render(request, 'django_app/news_API.html', {'news_data': news_data})
