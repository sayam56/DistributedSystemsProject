from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from django_app.form import SearchForm
import pandas as pd


# Create your views here.
def homepage(request):
    return render(request, 'django_app/homepage.html')


def searchView(request):
    searched_stock = None
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            searched_stock = form.cleaned_data['TickerName']
            ticker_value = form.cleaned_data['TickerName']
            number_of_days = form.cleaned_data['NumberofDays']
            return redirect('django_app:predict', ticker_value=ticker_value, number_of_days=number_of_days)
    else:
        form = SearchForm()
    return render(request, 'django_app/search.html', {'form': form, 'searched_stock': searched_stock})


def predict(request, ticker_value, number_of_days):
    ticker_value = ticker_value.upper()
    number_of_days = int(number_of_days)
    ticker = pd.read_csv('django_app/app/Tickers.csv')
    to_search = ticker_value
    for i in range(0, ticker.shape[0]):
        if ticker.Symbol[i] == to_search:
            Symbol = ticker.Symbol[i]
            Name = ticker.Name[i]
            break
    return render(request, "django_app/result.html", context={
                                                    'ticker_value':ticker_value,
                                                    'number_of_days':number_of_days,
                                                    'Symbol':Symbol,
                                                    'Name':Name,
                                                    })
