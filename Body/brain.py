import spacy
import re
import json
from Skills.weather_finder import Weather
from Skills.quotes import Quoter
from Skills.music import MusicPlayer
from Skills.apps import Appy
from Skills.date_and_time import DateTime
from Skills.lookup import LookUp

class Commands:
    
    # ----- Constants ----- #
    constants = json.load(f := open("./Commands/commands.json"))
    commands = constants['commands']
    thresholds = constants['thresholds']
    nlp = spacy.load('en_core_web_lg')
    
    
    # ----- Methods ----- #
    
    @staticmethod
    def most_similar(text: str, bias: str):
        text_nlp = Commands.nlp(text)
        max_sim = 0
        max_key = None
        
        for trigger in LookUp.get_triggers():
            if trigger in text:
                return 'SEARCH_PROMPT'
        
        for key, val in Commands.commands.items():
            curr_nlp = Commands.nlp(val)
            sim = text_nlp.similarity(curr_nlp)
            
            # Favours biased commands
            if bias and bias in key:
                sim += (1 - sim) / 4
                
            if sim > max_sim and sim > Commands.thresholds.get(key, 0.7):
                max_sim = sim
                max_key = key
        if max_sim < min(Commands.thresholds.values()):
            max_key = 'DEFAULT_RESPONSE'
        return max_key
    
    @staticmethod
    def parse_command(text: str):
        
        # Calculate biases
        bias = None
        if 'tomorrow' in text:
            bias = 'TOMORROW'
        elif 'time' in text:
            bias = 'TIME'
        elif 'weather' in text:
            bias = 'WEATHER'
        elif 'music' in text:
            bias = 'MUSIC' 

        command = Commands.most_similar(text, bias)
        extra = None

        if ('WEATHER' in command or 'TIME' in command):
            if loc := re.search(r'\bin\s\w+\b', text):
                start, end = loc.span()
                extra = text[start: end]
                extra = re.sub(r'\bin\s+', '', extra)
            else:
                extra = 'local'
        elif 'APP' in command:
            extra = text.replace('open', '').replace('close', '')
        elif 'SEARCH_PROMPT' in command:
            extra = text
            for t in LookUp.triggers:
                extra = extra.replace(f"{t} ", '')

        return command, extra
    
    @staticmethod
    def execute_command(command: str, extra):  # sourcery skip: low-code-quality
        
        location = extra if ('WEATHER' in command or 'TIME' in command) else None
        app = extra if 'APP' in command else None
        
        # Time
        
        if 'TIME_CURRENT' in command:
            return DateTime.get_time(location)
        
        elif 'DATE_CURRENT' in command:
            return DateTime.get_date()
        
        elif 'DAY_CURRENT' in command:
            return DateTime.get_day()
        
        # Weather

        elif 'CURRENT_WEATHER' in command:
            return Weather.get_current_weather_overview(location)
        
        elif 'CURRENT_TEMP' in command:
            return Weather.get_current_weather_specific('temperature', location)
        
        elif 'CURRENT_HUMIDITY' in command:
            return Weather.get_current_weather_specific('humidity', location)
        
        elif 'CURRENT_CLOUD' in command:
            return Weather.get_current_weather_specific('clouds', location)
        
        elif 'CURRENT_PRECIP' in command:
            return Weather.get_current_weather_specific('precip', location)
        
        elif 'CURRENT_WIND' in command:
            return Weather.get_current_weather_specific('windspeed', location)
        
        elif 'FORECAST_TOMORROW' in command:
            return Weather.get_weather_forecast_tomorrow(location)
        
        elif 'FORECAST_TODAY' in command:
            return Weather.get_weather_forecast_today(location)
        
        elif 'RAIN_TOMORROW' in command:
            return Weather.get_rain(location, 'tomorrow')
        
        elif 'RAIN_TODAY' in command:
            return Weather.get_rain(location, 'today')
        
        elif 'TEMP_TOMORROW' in command:
            return Weather.get_temp(location, 'tomorrow')
        
        elif 'TEMP_TODAY' in command:
            return Weather.get_temp(location, 'today')
        
        # Quotes
        elif 'QUOTE_INSPIRATIONAL' in command:
            return Quoter.inspire()
        
        # Music
        elif 'MUSIC_STUDY' in command:
            return MusicPlayer.play_study_music()
        
        elif 'MUSIC_STOP' in command:
            return MusicPlayer.stop_music()
        
        # Apps
        elif 'APP_OPEN' in command:
            return Appy.open_app(app)
            
        elif 'APP_CLOSE' in command:
            return Appy.close_app(app)
        
        # Search
        elif 'SEARCH_PROMPT' in command:
            return LookUp.search(extra)
        
        else:
            return Commands.commands['DEFAULT_RESPONSE']