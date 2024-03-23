from django.http import HttpResponse,HttpRequest
from django.shortcuts import render, redirect

from django.template.loader import render_to_string

from django_app.form import SearchForm


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

def search(request):
    searched_stock = None
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            searched_stock = form.cleaned_data['TickerName']
            ticker = form.cleaned_data['TickerName']
            days = form.cleaned_data['NumberofDays']
            return redirect('django_app:predict', ticker=ticker, days=days)
    else:
        form = SearchForm()
    return render(request, 'django_app/search.html', {'form': form, 'searched_stock': searched_stock})



import pandas as pd
def validate_ticker(ticker_input):
    df = pd.read_csv('django_app/Data/ticker_list.csv')
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
from plotly.io import json
import datetime as dt


def perform_prediction(ticker_value, forecast):
    # Assuming `forecast` is a list of predictions for the next `n` days
    pred_dict = {"Date": [], "Prediction": []}
    for i in range(0, len(forecast)):
        pred_dict["Date"].append(dt.datetime.today() + dt.timedelta(days=i))
        pred_dict["Prediction"].append(forecast[i])

    pred_df = pd.DataFrame(pred_dict)
    pred_fig = go.Figure([go.Scatter(x=pred_df['Date'], y=pred_df['Prediction'], mode='lines+markers')])
    pred_fig.update_xaxes(rangeslider_visible=True)
    pred_fig.update_layout(title=f"Stock Price Prediction for {ticker_value}",
                           paper_bgcolor="#14151b", plot_bgcolor="#14151b", font_color="white")
    plot_div_pred = plot(pred_fig, auto_open=False, output_type='div')

    return plot_div_pred


def get_ticker_info(ticker_value, csv_path='app/Data/Tickers.csv'):
    # Load the CSV file into a DataFrame
    ticker = pd.read_csv(csv_path)

    # Rename the columns to match the provided list
    ticker.columns = ['Symbol', 'Name', 'Last_Sale', 'Net_Change', 'Percent_Change', 'Market_Cap',
                      'Country', 'IPO_Year', 'Volume', 'Sector', 'Industry']

    # Use boolean indexing to find the row where the 'Symbol' matches 'ticker_value'
    ticker_row = ticker[ticker['Symbol'] == ticker_value]

    # If a match is found, return the information as a dictionary
    if not ticker_row.empty:
        ticker_info = ticker_row.iloc[0].to_dict()
        return ticker_info
    else:
        # Return None or an error message if no match is found
        return None

from sklearn.tree import DecisionTreeRegressor
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
def download_and_prepare_data(ticker_value, period='3mo', interval='1h', number_of_days=30):
    try:
        # Attempt to download the stock data
        df = yf.download(tickers=ticker_value, period=period, interval=interval)
    except Exception as e:
        print("Error downloading data:", e)
        return None

    # Keep only the 'Adj Close' column and calculate the future price as a new column
    df = df[['Adj Close']]
    df['Future Price'] = df[['Adj Close']].shift(-number_of_days)

    # Remove the last 'number_of_days' rows since they don't have a future price
    df = df[:-number_of_days]

    return df


def split_and_preprocess(df):
    # Features and labels
    X = df.drop(['Future Price'], axis=1).values
    y = df['Future Price'].values

    # Scaling features
    X_scaled = preprocessing.scale(X)

    # Splitting the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    return X_train, X_test, y_train, y_test


def predict_stock_prices(X_train, X_test, y_train, y_test):
    # Initialize the model
    model = DecisionTreeRegressor()

    # Train the model
    model.fit(X_train, y_train)

    # Test the model
    score = model.score(X_test, y_test)
    print("Model Confidence:", score)

    # Predictions
    predictions = model.predict(X_test)

    return predictions, score

def stock_prediction_view(request):
    if request.method == "POST":
        ticker_input="A"
        #ticker_input = request.POST.get("ticker", "").strip()
        #input_days = request.POST.get("days", "10").strip()

        # Validate the ticker
        # Assuming validate_ticker is adjusted to return a boolean or similar instead of HttpResponse
        if not validate_ticker(ticker_input):
            return render(request, 'Ticker_Unfounded.html')

        # Download data
        df=download_data(ticker_input)
        if df is None:
            return render(request,'yf_error.html')
        dates = df.index.strftime('%Y-%m-%d').tolist()
        closes = df['Close'].tolist()

        # Input days validation
        try:
            input_days=30
            #input_days=int(request.POST.get('days',10))
            if input_days<0:
                raise ValueError("Input days cannot be less than zero.")
            elif input_days>365:
                raise ValueError("Input days cannot be greater than 365")

        except ValueError as e:
            context = {'error': str(e)}
            return render(request, 'Input_Days_Error.html', context)

            # Prepare data for prediction
            #df_prepared = download_and_prepare_data('A', number_of_days=30)
            df_prepared = download_and_prepare_data(ticker_input, number_of_days=input_days)
            if df_prepared is not None:
                X_train, X_test, y_train, y_test = split_and_preprocess(df_prepared)
                predictions, confidence = predict_stock_prices(X_train, X_test, y_train, y_test)

                # Generating predictions for the future, not just the test set
                # This part of the code will need adjustments based on how you want to handle future predictions

                # For demonstration, let's assume predictions[-input_days:] gives us future predictions
                forecast_prediction = predictions[-input_days:]

                # Generate the prediction plot
                plot_div_pred = perform_prediction(ticker_input, forecast_prediction)
                context = {'plot_div_pred': plot_div_pred}
            else:
                context = {'error': "Failed to prepare data for prediction."}

            # Update context with additional information
            ticker_info = get_ticker_info(ticker_input)
            context.update({'chart_data': json.dumps({'dates': dates, 'closes': closes}), 'ticker_info': ticker_info})

        return render(request, "predict.html", context)

    # GET request or initial page load
    return render(request, "django_app/search.html")
