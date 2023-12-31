'''Aria's weather forecast functionality'''

import json
import geocoder
from Utilities.attempt_request import attempt_request

class Weather:
    '''Static class for finding weather details'''

    __API_KEY = None
    __BASE_URL = None
    __INITIALIZED = False

# -------------------- Main Functions -------------------- #

    @staticmethod
    def init():
        '''Initializes class API key'''
        try:
            with open('./data/keys.json', encoding='UTF-8') as keys:
                Weather.__API_KEY = json.load(keys)['WEATHER_API_KEY']
            Weather.__BASE_URL = "http://api.weatherapi.com/v1"
            Weather.__INITIALIZED = True
        except Exception:
            Weather.__INITIALIZED = False

# ----- Current Weather ----- #

    @staticmethod
    def get_current_weather_overview(location: str) -> str:
        '''Gets a general overview of current weather conditions'''
        if not Weather.__INITIALIZED:
            return "I'm sorry, my weather service is not working at the moment."

        if location == 'local':
            geo = geocoder.ip('me')
            location = f"{geo.latlng[0]},{geo.latlng[1]}"

        url = f"{Weather.__BASE_URL}/current.json?key={Weather.__API_KEY}&q={location}"
        response = attempt_request(url)

        # Could not make request (Internet issue?)
        if response is None:
            return "I'm sorry, something went wrong. \
                Are you sure your internet is working properly?"

        # Received error code
        if response.status_code != 200:
            return "I'm sorry, I'm running into some issues finding the weather conditions."

        # Successful request
        contents = response.json()
        details = {
            'location': f"{contents['location']['name']}, {contents['location']['country']}",
            'temperature': contents['current']['temp_c'],
            'feels_like': contents['current']['feelslike_c'],
            'humidity': contents['current']['humidity'],
            'windspeed': contents['current']['wind_kph'],
            'precip': contents['current']['precip_mm'],
            'clouds': cloud_percent_to_words(contents['current']['cloud'])
        }
        return current_details_to_words(details)

    @staticmethod
    def get_current_weather_specific(field: str, location: str) -> str:
        '''Gets a description of a particular weather condition'''
        if not Weather.__INITIALIZED:
            return "I'm sorry, my weather service is not working at the moment."

        if location == 'local':
            geo = geocoder.ip('me')
            location = f"{geo.latlng[0]},{geo.latlng[1]}"

        url = f"{Weather.__BASE_URL}/current.json?key={Weather.__API_KEY}&q={location}"
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
            return "I'm sorry, \
                I'm running into some issues finding the weather conditions."

        # Successful request
        contents = response.json()
        details = {
            'location': f"{contents['location']['name']}, {contents['location']['country']}",
            'temperature': contents['current']['temp_c'],
            'feels_like': contents['current']['feelslike_c'],
            'humidity': contents['current']['humidity'],
            'windspeed': contents['current']['wind_kph'],
            'precip': contents['current']['precip_mm'],
            'clouds': cloud_percent_to_words(contents['current']['cloud'])
        }

        return current_weather_condition_to_words(field, details)

    # ----- Forecasting ----- #

    @staticmethod
    def get_weather_forecast_tomorrow(location: str) -> str:
        '''Gets tomorrows forecast for anywhere world-wide'''
        if not Weather.__INITIALIZED:
            return "I'm sorry, my weather service is not working at the moment."

        if location == 'local':
            geo = geocoder.ip('me')
            location = f"{geo.latlng[0]},{geo.latlng[1]}"

        url = f"{Weather.__BASE_URL}/forecast.json?key={Weather.__API_KEY}&q={location}&days=2"
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
            return "I'm sorry, I'm running into some issues finding the weather conditions."

        # Successful request
        loc = f"{response.json()['location']['name']}, {response.json()['location']['country']}"
        contents = response.json()['forecast']['forecastday'][1]
        details = {
            'location': loc,
            'max_temp': contents['day']['maxtemp_c'],
            'min_temp': contents['day']['mintemp_c'],
            'avg_temp': contents['day']['avgtemp_c'],
            'chance_of_rain': calc_chance_of_rain(contents['hour']),
            'humidity': int(contents['day']['avghumidity']),
            'clouds': cloud_percent_to_words(calc_average_cloud_cover(contents['hour']))
        }
        return forecast_details_to_words(details, "Tomorrow")

    @staticmethod
    def get_weather_forecast_today(location: str) -> str:
        '''Gets todays forecast for anywhere world-wide'''
        if not Weather.__INITIALIZED:
            return "I'm sorry, my weather service is not working at the moment."

        if location == 'local':
            geo = geocoder.ip('me')
            location = f"{geo.latlng[0]},{geo.latlng[1]}"

        url = f"{Weather.__BASE_URL}/forecast.json?key={Weather.__API_KEY}&q={location}"
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
            return "I'm sorry, I'm running into some issues finding the weather conditions."

        # Successful request
        loc = f"{response.json()['location']['name']}, {response.json()['location']['country']}"
        contents = response.json()['forecast']['forecastday'][0]
        details = {
            'location': loc,
            'max_temp': contents['day']['maxtemp_c'],
            'min_temp': contents['day']['mintemp_c'],
            'avg_temp': contents['day']['avgtemp_c'],
            'chance_of_rain': calc_chance_of_rain(contents['hour']),
            'humidity': int(contents['day']['avghumidity']),
            'clouds': cloud_percent_to_words(calc_average_cloud_cover(contents['hour']))
        }
        return forecast_details_to_words(details, "Today")

    @staticmethod
    def get_rain(location: str, day: str) -> str:
        '''Checks how likely it is to rain today ot tomorrow'''
        if not Weather.__INITIALIZED:
            return "I'm sorry, my weather service is not working at the moment."

        tday = 0 if day.lower() == 'today' else 1

        if location == 'local':
            geo = geocoder.ip('me')
            location = f"{geo.latlng[0]},{geo.latlng[1]}"

        url = f"{Weather.__BASE_URL}/forecast.json?key={Weather.__API_KEY}&q={location}&days=2"
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
            return "I'm sorry, I'm running into some issues finding the weather conditions."

        # Successful request
        loc = f"{response.json()['location']['name']}, {response.json()['location']['country']}"
        contents = response.json()['forecast']['forecastday'][tday]
        rain_chance = calc_chance_of_rain(contents['hour'])
        return f"{day.title()} in {loc}, there is a {rain_chance}% chance of rain."

    @staticmethod
    def get_temp(location: str, day: str) -> str:
        '''Checks how hot it will be today or tomorrow'''
        if not Weather.__INITIALIZED:
            return "I'm sorry, my weather service is not working at the moment."

        tday = 0 if day.lower() == 'today' else 1

        if location == 'local':
            geo = geocoder.ip('me')
            location = f"{geo.latlng[0]},{geo.latlng[1]}"

        url = f"{Weather.__BASE_URL}/forecast.json?key={Weather.__API_KEY}&q={location}&days=2"
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
            return "I'm sorry, I'm running into some issues finding the weather conditions."

        # Successful request
        loc = f"{response.json()['location']['name']}, {response.json()['location']['country']}"
        contents = response.json()['forecast']['forecastday'][tday]
        avg_temp = contents['day']['avgtemp_c']
        min_temp = contents['day']['mintemp_c']
        max_temp = contents['day']['maxtemp_c']

        output = f"{day.title()} in {loc}, the average temperature will be \
            {avg_temp} degrees celsius, with a low of {min_temp} and a high of {max_temp}."
        if day.lower() == 'today':
            output = output.replace('will be', 'is')
        return output

# -------------------- Supplementary Functions -------------------- #

# ----- Weather Calculations ----- #

def calc_chance_of_rain(hours: list[dict]) -> int:
    '''Calculates daily chance of rain from hourly chances'''
    chance_no_rain = 1
    for hour in hours:
        chance_no_rain *= (1 - (hour['chance_of_rain'] / 100))
    return int((1 - chance_no_rain) * 100)

def calc_average_cloud_cover(hours: list[dict]) -> int:
    '''Calculates a days average cloud cover'''
    return sum(hour['cloud'] for hour in hours) // len(hours)


# ----- Translate To Words ----- #

def cloud_percent_to_words(coverage: int) -> str:
    '''Gets the cloud cover description from percentage'''
    if coverage is None:
        return None

    if coverage >= 90:
        return "overcast"
    if coverage >= 65:
        return "mostly cloudy"
    if coverage >= 35:
        return "partly cloudy"
    return "fair skies" if coverage > 10 else "clear skies"

def current_details_to_words(details: dict) -> str:
    '''Converts current weather conditions to words'''
    output = f"In {details['location']} it is currently {details['temperature']} degrees celcius"
    output += f", but it feels like it's {details['feels_like']} degrees." \
        if details['feels_like'] else "."
    output += f" It is {details['clouds']}"
    output += f", with {details['precip']} milimeters of precipitation." \
        if details['precip'] else "."
    output += f" The current humidity is {details['humidity']}%"
    output += f", and the average windspeed is {details['windspeed']} kilometers per hour." \
        if details['windspeed'] else "."
    return output

def forecast_details_to_words(details: dict, day: str) -> str:
    '''Converts a forecast to words'''
    output = f"{day} in {details['location']}, the average temperature will be \
        {details['avg_temp']} degrees celcius, "
    output += f"with a low of {details['min_temp']} and a high of {details['max_temp']}. "
    output += f"The average humidity will be {details['humidity']}%, "
    output += f"and it will be {details['clouds']} with a \
        {details['chance_of_rain']}% chance of rain."
    if day.lower() == 'today':
        output = output.replace('will be', 'is')
    return output

def current_weather_condition_to_words(field: str, details: dict) -> str:
    '''Converts a weather condition to words'''
    if field not in details:
        return "Sorry, I can't find the field you're looking for."

    if field == 'temperature':
        return f"In {details['location']} it is currently {details[field]} degrees celcius."
    if field == 'feels_like':
        return f"In {details['location']} it feels like it's {details[field]} degrees celcius."
    if field == 'humidity':
        return f"In {details['location']} the humidity is {details[field]}% at the moment."
    if field == 'windspeed':
        return f"In {details['location']} the wind is blowing at \
            {details[field]} kilometers per hour."
    if field == 'precip':
        return f"{details['location']} is currently receiving \
            {details[field]} milimeters of precipitation."
    return f"It is currently {details[field]} in {details['location']}."
