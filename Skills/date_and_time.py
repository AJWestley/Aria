'''Aria's date and time functions'''

from datetime import datetime
import json
import pytz
from Utilities.attempt_request import attempt_request

class DateTime:
    '''Static class for getting date and time data'''

    __API_KEY = None
    __BASE_URL = None
    __INITIALIZED = False

    @staticmethod
    def init():
        '''Initializes class API key'''
        try:
            with open('./data/keys.json', encoding='UTF-8') as keys:
                DateTime.__API_KEY = json.load(keys)['WEATHER_API_KEY']
            DateTime.__BASE_URL = "http://api.weatherapi.com/v1"
            DateTime.__INITIALIZED = True
        except Exception:
            DateTime.__INITIALIZED = False

    @staticmethod
    def get_time(location: str):
        '''Finds the time locally or in a specific location'''
        if location == 'local':
            time = datetime.now()
            return f" It is {time.strftime('%H:%M')}."

        if not DateTime.__INITIALIZED:
            return "I'm sorry, my timezone service is not working at the moment."

        url = f"{DateTime.__BASE_URL}/current.json?key={DateTime.__API_KEY}&q={location}"
        response = attempt_request(url)

        # Could not make request (Internet issue?)
        if response is None:
            return "I'm sorry, something went wrong. \
                Are you sure your internet is working properly?"

        # Received error code
        if response.status_code != 200:
            error_code = response.json()['error']['code']
            if error_code == 1006:
                return "I'm sorry, I could not find the location you asked for."
            return "I'm sorry, I'm running into some issues finding the time at that location."

        # Successful request
        contents = response.json()
        timezone = pytz.timezone(contents['location']['tz_id'])
        time = datetime.now(timezone)
        return f" It is {time.strftime('%H:%M')} in {location}."

    @staticmethod
    def get_date():
        '''Gets the current date'''
        today = datetime.now().strftime("%d %B %Y")
        return f"Todays date is {today}."

    @staticmethod
    def get_day():
        '''Gets the current day of the week'''
        day = datetime.now().strftime("%A")
        return f"Today is {day}."
