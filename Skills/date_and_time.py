import pytz
from datetime import datetime
import os
from Utilities.attempt_request import attempt_request

class DateTime:

    __API_KEY = os.environ["WEATHER_API_KEY"]
    __BASE_URL = "http://api.weatherapi.com/v1"

    @staticmethod
    def get_time(location: str):
        if location == 'local':
            time = datetime.now()
            return f" It is {time.strftime('%H:%M')}."
        
        url = f"{DateTime.__BASE_URL}/current.json?key={DateTime.__API_KEY}&q={location}"
        response = attempt_request(url)
        
        # Could not make request (Internet issue?)
        if response is None:
            return "I'm sorry, something went wrong. Are you sure your internet is working properly?"
        
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
        today = datetime.now().strftime("%d %B %Y")
        return f"Todays date is {today}."

    @staticmethod
    def get_day():
        d = datetime.now().strftime("%A")
        return f"Today is {d}."