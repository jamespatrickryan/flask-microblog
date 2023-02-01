import requests

from flask import current_app

from flask_babel import _


def translate(text, source_language, destination_language):
    if 'X_RAPIDAPI_KEY' not in current_app.config:
        return _('Error: Translation service not configured.')

    url = 'https://rapid-translate-multi-traduction.p.rapidapi.com/t'
    payload = {
        'from': source_language,
        'to': destination_language,
        'e': '',
        'q': text
    }
    headers = {
        'content-type': 'application/json',
        'X-RapidAPI-Key': current_app.config['X_RAPIDAPI_KEY'],
        'X-RapidAPI-Host': 'rapid-translate-multi-traduction.p.rapidapi.com'
    }

    response = requests.request('POST', url, json=payload, headers=headers)

    if response.status_code != 200:
        return _('Error: Translation service failed.')
    return response.json()[0]
