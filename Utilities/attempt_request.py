'''Attempts to send a request to a url'''

import requests as r

def attempt_request(url: str):
    response = None
    try:
        response = r.get(url, timeout=10)
    except r.exceptions.RequestException:
        response = None
    return response
