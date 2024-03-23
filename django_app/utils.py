import requests

from django_app.models import Favourite


def get_news():
    url = 'https://api.marketaux.com/v1/news/all'
    headers = {
        'Authorization': 'Bearer 659FVmRJ98V2UbhRN2Rdr6irbuO2k6Ckb29KS0MB'
    }
    favourite_symbols = Favourite.objects.values_list('stock__symbol', flat=True)

    params = {
        'symbols': ','.join(favourite_symbols),
        "sentiment_gte": 0.1,
        'filter_entities': 'true',
        'language': 'en',

    }
#GET https://api.marketaux.com/v1/news/all?sentiment_gte=0.1&language=en&api_token=659FVmRJ98V2UbhRN2Rdr6irbuO2k6Ckb29KS0MB
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        # Handle errors, raise exceptions, etc.
        response.raise_for_status()
