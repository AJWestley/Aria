from attempt_request import attempt_request
import geocoder
import os

class Weather:

    __API_KEY = os.environ["WEATHER_API_KEY"]
    __BASE_URL = "http://api.weatherapi.com/v1"

# -------------------- Main Functions -------------------- #

# ----- Current Weather ----- #

    @staticmethod
    def get_current_weather_overview(location: str) -> str:
        
        if location == 'local':
            g = geocoder.ip('me')
            location = f"{g.latlng[0]},{g.latlng[1]}"
        
        url = f"{Weather.__BASE_URL}/current.json?key={Weather.__API_KEY}&q={location}"
        response = attempt_request(url)
        
        # Could not make request (Internet issue?)
        if response is None:
            return "I'm sorry, something went wrong. Are you sure your internet is working properly?"
        
        # Received error code
        if response.status_code != 200:
            error_code = response.json()['error']['code']
            if error_code == 1006:
                return "I'm sorry, I could not find the location you asked for."
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
            'clouds': __cloud_percent_to_words(contents['current']['cloud'])
        }
        
        return __current_details_to_words(details)

    @staticmethod
    def get_current_weather_specific(field: str, location: str) -> str:
        
        if location == 'local':
            g = geocoder.ip('me')
            location = f"{g.latlng[0]},{g.latlng[1]}"
        
        url = f"{Weather.__BASE_URL}/current.json?key={Weather.__API_KEY}&q={location}"
        response = attempt_request(url)

        # Could not make request (Internet issue?)
        if response is None:
            return "I'm sorry, something went wrong. Are you sure your internet is working properly?"

        # Received error code
        if response.status_code != 200:
            error_code = response.json()['error']['code']
            if error_code == 1006:
                return "I'm sorry, I could not find the location you asked for."
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
            'clouds': __cloud_percent_to_words(contents['current']['cloud'])
        }

        return __current_weather_condition_to_words(field, details)

    # ----- Forecasting ----- #

    @staticmethod
    def get_weather_forecast_tomorrow(location: str) -> str:
        
        if location == 'local':
            g = geocoder.ip('me')
            location = f"{g.latlng[0]},{g.latlng[1]}"
        
        url = f"{Weather.__BASE_URL}/forecast.json?key={Weather.__API_KEY}&q={location}&days=2"
        response = attempt_request(url)
        
        # Could not make request (Internet issue?)
        if response is None:
            return "I'm sorry, something went wrong. Are you sure your internet is working properly?"
        
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
            'chance_of_rain': __calc_chance_of_rain(contents['hour']),
            'humidity': int(contents['day']['avghumidity']),
            'clouds': __cloud_percent_to_words(__calc_average_cloud_cover(contents['hour']))
        }
        return __forecast_details_to_words(details, "Tomorrow")

    @staticmethod
    def get_weather_forecast_today(location: str) -> str:
        
        if location == 'local':
            g = geocoder.ip('me')
            location = f"{g.latlng[0]},{g.latlng[1]}"
        
        url = f"{Weather.__BASE_URL}/forecast.json?key={Weather.__API_KEY}&q={location}"
        response = attempt_request(url)
        
        # Could not make request (Internet issue?)
        if response is None:
            return "I'm sorry, something went wrong. Are you sure your internet is working properly?"
        
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
            'chance_of_rain': __calc_chance_of_rain(contents['hour']),
            'humidity': int(contents['day']['avghumidity']),
            'clouds': __cloud_percent_to_words(__calc_average_cloud_cover(contents['hour']))
        }
        return __forecast_details_to_words(details, "Today")

    @staticmethod
    def get_rain(location: str, day: str) -> str:
        
        d = 0 if day.lower() == 'today' else 1
        
        if location == 'local':
            g = geocoder.ip('me')
            location = f"{g.latlng[0]},{g.latlng[1]}"
        
        url = f"{Weather.__BASE_URL}/forecast.json?key={Weather.__API_KEY}&q={location}&days=2"
        response = attempt_request(url)
        
        # Could not make request (Internet issue?)
        if response is None:
            return "I'm sorry, something went wrong. Are you sure your internet is working properly?"
        
        # Received error code
        if response.status_code != 200:
            error_code = response.json()['error']['code']
            if error_code == 1006:
                return "I'm sorry, I could not find the location you asked for."
            return "I'm sorry, I'm running into some issues finding the weather conditions."
        
        # Successful request
        loc = f"{response.json()['location']['name']}, {response.json()['location']['country']}"
        contents = response.json()['forecast']['forecastday'][d]
        rain_chance = __calc_chance_of_rain(contents['hour'])
        return f"{day.title()} in {loc}, there is a {rain_chance}% chance of rain."

    @staticmethod
    def get_temp(location: str, day: str) -> str:
        
        d = 0 if day.lower() == 'today' else 1
        
        if location == 'local':
            g = geocoder.ip('me')
            location = f"{g.latlng[0]},{g.latlng[1]}"
        
        url = f"{Weather.__BASE_URL}/forecast.json?key={Weather.__API_KEY}&q={location}&days=2"
        response = attempt_request(url)
        
        # Could not make request (Internet issue?)
        if response is None:
            return "I'm sorry, something went wrong. Are you sure your internet is working properly?"
        
        # Received error code
        if response.status_code != 200:
            error_code = response.json()['error']['code']
            if error_code == 1006:
                return "I'm sorry, I could not find the location you asked for."
            return "I'm sorry, I'm running into some issues finding the weather conditions."
        
        # Successful request
        loc = f"{response.json()['location']['name']}, {response.json()['location']['country']}"
        contents = response.json()['forecast']['forecastday'][d]
        avg_temp = contents['day']['avgtemp_c']
        min_temp = contents['day']['mintemp_c']
        max_temp = contents['day']['maxtemp_c']
        
        output = f"{day.title()} in {loc}, the average temperature will be {avg_temp} degrees celsius, with a low of {min_temp} and a high of {max_temp}."
        if day.lower() == 'today':
            output = output.replace('will be', 'is')
        return output

# -------------------- Supplementary Functions -------------------- #

# ----- Weather Calculations ----- #

def __calc_chance_of_rain(hours: list[dict]) -> int:
    chance_no_rain = 1
    for hour in hours:
        chance_no_rain *= (1 - (hour['chance_of_rain'] / 100))
    return int((1 - chance_no_rain) * 100)

def __calc_average_cloud_cover(hours: list[dict]) -> int:
    return sum(hour['cloud'] for hour in hours) // len(hours)
    

# ----- Translate To Words ----- #

def __cloud_percent_to_words(coverage: int) -> str:
    if coverage is None: 
        return None

    if coverage >= 90:
        return "overcast"
    elif coverage >= 65:
        return "mostly cloudy"
    elif coverage >= 35:
        return "partly cloudy"
    elif coverage > 10:
        return "fair skies"
    return "clear skies"

def __current_details_to_words(details: dict) -> str:
    output = f"In {details['location']} it is currently {details['temperature']} degrees celcius"
    output += f", but it feels like it's {details['feels_like']} degrees." if details['feels_like'] else "."
    output += f" It is {details['clouds']}"
    output += f", with {details['precip']} milimeters of precipitation." if details['precip'] else "."
    output += f" The current humidity is {details['humidity']}%"
    output += f", and the average windspeed is {details['windspeed']} kilometers per hour." if details['windspeed'] else "."
    return output

def __forecast_details_to_words(details: dict, day: str) -> str:
    output = f"{day} in {details['location']}, the average temperature will be {details['avg_temp']} degrees celcius, "
    output += f"with a low of {details['min_temp']} and a high of {details['max_temp']}. "
    output += f"The average humidity will be {details['humidity']}%, "
    output += f"and it will be {details['clouds']} with a {details['chance_of_rain']}% chance of rain."
    if day.lower() == 'today':
        output = output.replace('will be', 'is')
    return output

def __current_weather_condition_to_words(field: str, details: dict) -> str:
    if field not in details:
        return "Sorry, I can't find the field you're looking for."
    
    if field == 'temperature':
        return f"In {details['location']} it is currently {details[field]} degrees celcius."
    elif field == 'feels_like':
        return f"In {details['location']} it feels like it's {details[field]} degrees celcius."
    elif field == 'humidity':
        return f"In {details['location']} the humidity is {details[field]}% at the moment."
    elif field == 'windspeed':
        return f"In {details['location']} the wind is blowing at {details[field]} kilometers per hour."
    elif field == 'precip':
        return f"{details['location']} is currently receiving {details[field]} milimeters of precipitation."
    return f"It is currently {details[field]} in {details['location']}."

