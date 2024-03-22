from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import DetailView

from django_app.form import SearchForm
import pandas as pd

from django_app.models import News


# Create your views here.
def homepage(request):
    return render(request, 'django_app/homepage.html')


def searchView(request):
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


def predict(request, ticker, days):
    ticker_info = ticker
    days_number = int(days)
    tickers = pd.read_csv('django_app/app/Tickers.csv')
    for i in range(0, tickers.shape[0]):
        if tickers.Symbol[i] == ticker_info:
            Symbol = tickers.Symbol[i]
            Name = tickers.Name[i]
            break
    return render(request, "django_app/result.html", context={
                                                    'ticker_info':ticker_info,
                                                    'days_number':days_number,
                                                    'Symbol':Symbol,
                                                    'Name':Name,
                                                    })


class newsView(View):
    template_name = 'django_app/news.html'

    def get(self, request):
        news = News.objects.all()
        context = {
            'news': news,
        }

        return render(request, self.template_name, context)
