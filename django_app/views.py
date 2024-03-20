from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
import pandas as pd
import json

# Create your views here.
def homepage(request):
    return render(request, 'django_app/homepage.html')


def ticker(request):
    # ================================================= Load Ticker Table ================================================
    ticker_df = pd.read_csv('django_app/Data/new_tickers.csv')
    json_ticker = ticker_df.reset_index().to_json(orient ='records')
    ticker_list = []
    ticker_list = json.loads(json_ticker)


    return render(request, 'django_app/ticker.html', {
        'ticker_list': ticker_list
    })
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
