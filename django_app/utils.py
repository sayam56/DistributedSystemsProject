import requests


def get_news():
    url = 'https://api.marketaux.com/v1/news/all'
    headers = {
        'Authorization': 'Bearer 659FVmRJ98V2UbhRN2Rdr6irbuO2k6Ckb29KS0MB'
    }
    params = {
        'symbols': 'TSLA,AMZN,MSFT',
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
