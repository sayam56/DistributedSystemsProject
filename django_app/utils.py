import requests


def get_news():
    url = 'https://api.marketaux.com/v1/news/all'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer 659FVmRJ98V2UbhRN2Rdr6irbuO2k6Ckb29KS0MB',
        # Add any necessary authentication headers if required
    }
    params = {
        'language': 'en',
        'symbols': 'ONGC,TSLA',
        'filter_entities': 'true',
        'sentiment_gte': '0.1',
        'entity_types': 'index,equity',
    }
#GET https://api.marketaux.com/v1/news/all?sentiment_gte=0.1&language=en&api_token=659FVmRJ98V2UbhRN2Rdr6irbuO2k6Ckb29KS0MB
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        # Handle errors, raise exceptions, etc.
        response.raise_for_status()
