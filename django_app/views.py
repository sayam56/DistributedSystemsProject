from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
import pandas as pd
import json
from django.urls import reverse_lazy, reverse
from urllib import request
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import RequestContext
from django.views import View, generic
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import StockSearch, SignupForm
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
    # Left Card Plot
    # Here we used yf.download function
    data = yf.download(
        # passes the ticker
        tickers=['AAPL', 'AMZN', 'QCOM', 'META', 'NVDA', 'GOOGL', 'UBER', 'TSLA'],

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
        go.Scatter(x=data['Date'], y=data['GOOGL']['Adj Close'], name="GOOGL")
    )
    fig_left.add_trace(
        go.Scatter(x=data['Date'], y=data['UBER']['Adj Close'], name="UBER")
    )
    fig_left.add_trace(
        go.Scatter(x=data['Date'], y=data['TSLA']['Adj Close'], name="TSLA")
    )
    fig_left.update_layout(paper_bgcolor="#14151b", plot_bgcolor="#14151b", font_color="white")

    plot_div_left = plot(fig_left, auto_open=False, output_type='div')

    # ================================================ To show recent stocks ==============================================

    df1 = yf.download(tickers='AAPL', period='1d', interval='1d')
    df2 = yf.download(tickers='AMZN', period='1d', interval='1d')
    df3 = yf.download(tickers='QCOM', period='1d', interval='1d')
    df4 = yf.download(tickers='META', period='1d', interval='1d')
    df5 = yf.download(tickers='NVDA', period='1d', interval='1d')
    df6 = yf.download(tickers='GOOGL', period='1d', interval='1d')
    df7 = yf.download(tickers='UBER', period='1d', interval='1d')
    df8 = yf.download(tickers='TSLA', period='1d', interval='1d')
    # df6 = yf.download(tickers='TWTR', period='1d', interval='1d')

    df1.insert(0, "Ticker", "AAPL")
    df2.insert(0, "Ticker", "AMZN")
    df3.insert(0, "Ticker", "QCOM")
    df4.insert(0, "Ticker", "META")
    df5.insert(0, "Ticker", "NVDA")
    df6.insert(0, "Ticker", "GOOGL")
    df7.insert(0, "Ticker", "UBER")
    df8.insert(0, "Ticker", "TSLA")
    # df6.insert(0, "Ticker", "TWTR")

    df = pd.concat([df1, df2, df3, df4, df5, df6, df7, df8], axis=0)
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


@login_required
def predict(request):
    response = HttpResponse()
    heading1 = '<p>' + 'PREDICT PAGE:' + '</p>'
    response.write(heading1)

    return response


def stockInfo(request):
    # Load Ticker Table
    ticker_df = pd.read_csv('django_app/Data/new_tickers.csv')

    # Get the query (if it exists)
    query = request.GET.get('q')
    no_results = False

    if query:
        # Filter the DataFrame based on the query
        ticker_df = ticker_df[ticker_df['Symbol'].str.contains(query, case=False)]

        if ticker_df.empty:
            no_results = True

    ticker_list = ticker_df.to_dict('records')  # Convert DataFrame to list of dicts

    # provided by JIYU
    # Set up pagination - 18 rows per page
    page = request.GET.get('page', 1)  # Get the page number from the request
    paginator = Paginator(ticker_list, 18)  # Instantiate Paginator with 40 items per page

    try:
        tickers = paginator.page(page)  # Get the page of tickers
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        tickers = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        tickers = paginator.page(paginator.num_pages)

    # Create an instance of the form
    form = StockSearch(request.GET)

    return render(request, 'django_app/ticker.html', {
        'ticker_list': tickers,
        'no_results': no_results,
        'form': form
    })


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


#################################################################################################################
#################################################################################################################
#################################################################################################################
from django_app.forms import SearchForm
def search(request):
    searched_stock = None
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            searched_stock = form.cleaned_data['TickerName']
            ticker = form.cleaned_data['TickerName']
            days = form.cleaned_data['NumberofDays']

            # Check if the number of days is within the valid range
            if 0 <= days <= 365:
                return redirect('django_app:stock_prediction_view', ticker=ticker, days=days)
            else:
                # Handle invalid days
                return render(request, 'django_app/Input_Days_Error.html', {'error': "Input days must be between 0 and 365."})
    else:
        form = SearchForm()
    return render(request, 'django_app/search.html', {'form': form, 'searched_stock': searched_stock})

import pandas as pd
def validate_ticker(ticker_input):
    df = pd.read_csv('django_app/Data/new_tickers.csv')
    symbols_list = df['Symbol'].tolist()
    valid_tickers = symbols_list
    #tickers are all uppercase
    ticker_upper_value = ticker_input.upper()
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


def perform_prediction(ticker_value, forecast, last_date):
    pred_dict = {"Date": [], "Prediction": []}
    start_date = pd.to_datetime(last_date)
    for i in range(len(forecast)):
        pred_dict["Date"].append(start_date + pd.Timedelta(days=i))
        pred_dict["Prediction"].append(forecast[i])

    pred_df = pd.DataFrame(pred_dict)
    pred_fig = go.Figure([go.Scatter(x=pred_df['Date'], y=pred_df['Prediction'], mode='lines+markers')])
    pred_fig.update_xaxes(rangeslider_visible=True)
    pred_fig.update_layout(title=f"Stock Price Prediction for {ticker_value}",
                           xaxis=dict(rangeslider=dict(visible=True), type="date"),
                           paper_bgcolor="#14151b", plot_bgcolor="#14151b", font_color="white")
    plot_div_pred = plot(pred_fig, auto_open=False, output_type='div')

    return plot_div_pred


def get_ticker_info(ticker_value, csv_path='django_app/Data/Tickers.csv'):
    ticker = pd.read_csv(csv_path)

    # Rename the columns to match the provided list
    ticker.columns = ['Symbol', 'Name', 'Last_Sale', 'Net_Change', 'Percent_Change', 'Market_Cap',
                      'Country', 'IPO_Year', 'Volume', 'Sector', 'Industry']

    ticker_row = ticker[ticker['Symbol'] == ticker_value]

    if not ticker_row.empty:
        ticker_info = ticker_row.iloc[0].to_dict()
        return ticker_info
    else:
        return None

from sklearn.tree import DecisionTreeRegressor
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
def download_and_prepare_data(ticker_value, period='3mo', interval='1h', number_of_days=30):
    try:
        df = yf.download(tickers=ticker_value, period=period, interval=interval)
    except Exception as e:
        print("Error downloading data:", e)
        return None

    df = df[['Adj Close']]
    df['Future Price'] = df[['Adj Close']].shift(-number_of_days)

    df = df[:-number_of_days]

    return df


def split_and_preprocess(df):
    # Features and labels
    X = df.drop(['Future Price'], axis=1).values
    y = df['Future Price'].values

    X_scaled = preprocessing.scale(X)

    # Splitting the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    return X_train, X_test, y_train, y_test


def predict_stock_prices(X_train, X_test, y_train, y_test):
    model = DecisionTreeRegressor()

    # Train the model
    model.fit(X_train, y_train)

    score = model.score(X_test, y_test)
    print("Model Confidence:", score)

    # Predictions
    predictions = model.predict(X_test)

    return predictions, score

def create_recent_stock_price_chart(dates, closes, ticker_value):
    # Create a Plotly figure
    recent_fig = go.Figure(data=[go.Scatter(x=dates, y=closes, mode='lines+markers')])
    recent_fig.update_layout(title=f"Recent Stock Price of {ticker_value}",
                             xaxis_title="Date",
                             yaxis_title="Stock Price",
                             paper_bgcolor="#14151b",
                             plot_bgcolor="#14151b",
                             font_color="white")

    # Generate HTML div containing the plot
    plot_div_live = plot(recent_fig, auto_open=False, output_type='div')

    return plot_div_live

def stock_prediction_view(request, ticker, days):
    # Convert days from string to integer
    try:
        input_days = int(days)
    except ValueError:
        return render(request, 'django_app/Input_Days_Error.html', {'error': "Invalid number of days."})

    if input_days < 1 or input_days > 365:
        return render(request, 'django_app/Input_Days_Error.html', {'error': "Input days must be between 0 and 365."})

    if not validate_ticker(ticker):
        return render(request, 'django_app/Ticker_Unfounded.html')

    df = download_data(ticker)
    if df is None:
        return render(request, 'django_app/yf_error.html')

    last_date = df.index[-1].strftime('%Y-%m-%d %H:%M:%S')
    dates = df.index.strftime('%Y-%m-%d %H:%M:%S').tolist()
    closes = df['Close'].tolist()
    #print(dates)
    #print(closes)
    context = {'chart_data':json.dumps({'dates': dates, 'closes': closes})}
    plot_div_live = create_recent_stock_price_chart(dates, closes, ticker)
    #print(plot_div_live)
    context.update({'plot_div_live': plot_div_live})

    # Prepare data for prediction
    df_prepared = download_and_prepare_data(ticker, number_of_days=input_days)
    if df_prepared is not None:
        X_train, X_test, y_train, y_test = split_and_preprocess(df_prepared)
        predictions, confidence = predict_stock_prices(X_train, X_test, y_train, y_test)
        forecast_prediction = predictions[-input_days:]

        plot_div_pred = perform_prediction(ticker, forecast_prediction,last_date)
        context.update({'plot_div_pred': plot_div_pred})
    else:
        context.update({'error': "Failed to prepare data for prediction."})

    ticker_info = get_ticker_info(ticker)
    #print(ticker_info)

    context.update({
        'ticker_info': ticker_info,
        'days':days,
    })
    #print(context)
    return render(request, "django_app/predict.html", context)
