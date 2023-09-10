import requests as r

def attempt_request(url: str):
    response = None
    try:
        response = r.get(url)
    except r.exceptions.RequestException as e:
        response = None
    return response