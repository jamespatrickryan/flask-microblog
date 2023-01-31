import requests

from flask_babel import _

from app import app


def translate(text, destination_language):
    if 'X_RAPIDAPI_KEY' not in app.config:
        return _('Error: Translation service not configured.')

    url = 'https://microsoft-translator-text.p.rapidapi.com/translate'
    payload = [{'Text': text}]
    headers = {
        'content-type': 'application/json',
        'X-RapidAPI-Key': app.config['X_RAPIDAPI_KEY'],
        'X-RapidAPI-Host': 'microsoft-translator-text.p.rapidapi.com'
    }

    query_string = {
        'to[0]': destination_language,
        'api-version': '3.0',
        'profanityAction': 'NoAction',
        'textType': 'plain'
    }

    response = requests.request('POST', url, json=payload, headers=headers,
                                params=query_string)
    if response.status_code != 200:
        return _('Error: Translation service failed.')
    return response.json()[0]['translations'][0]['text']
