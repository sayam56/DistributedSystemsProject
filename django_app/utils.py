import requests

from django_app.models import Favourite


def get_news(user=None):
    url = 'https://api.marketaux.com/v1/news/all'
    headers = {
        'Authorization': 'Bearer 659FVmRJ98V2UbhRN2Rdr6irbuO2k6Ckb29KS0MB'
    }

    if user is not None:
        favourite_symbols = Favourite.objects.filter(user=user).values_list('stock__symbol', flat=True)
    else:
        favourite_symbols = 'ONGC, AAPL, GOOGL, META'

    params = {
        'symbols': ','.join(favourite_symbols),
        "sentiment_gte": 0.1,
        'filter_entities': 'true',
        'language': 'en',
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()
