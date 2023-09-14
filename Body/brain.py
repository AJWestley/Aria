'''Aria's Task Mode brain'''

import re
import json
import spacy
from Skills.weather_finder import Weather
from Skills.quotes import Quoter
from Skills.music import MusicPlayer
from Skills.apps import Appy
from Skills.date_and_time import DateTime
from Skills.lookup import LookUp

class Commands:
    '''Static class for parsing and executing commands'''

    # ----- Constants ----- #
    commands = None
    thresholds = None
    nlp = spacy.load('en_core_web_lg')
    __INITIALIZED = False


    # ----- Methods ----- #
    @staticmethod
    def init():
        '''Initializes the class and its constituents'''

        Weather.init()
        DateTime.init()

        try:
            with open("./data/commands.json", encoding='UTF-8') as cmds:
                constants = json.load(cmds)
                Commands.commands = constants['commands']
                Commands.thresholds = constants['thresholds']
            Commands.__INITIALIZED = True
        except Exception:
            Commands.__INITIALIZED = False

    @staticmethod
    def __most_similar(text: str, bias: str):
        '''Finds most similar command to a given instruction'''
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
        '''Takes an instruction and turns it into a command'''
        if not Commands.__INITIALIZED:
            return None, None

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

        command = Commands.__most_similar(text, bias)
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
            for trig in LookUp.triggers:
                extra = extra.replace(f"{trig} ", '')

        return command, extra

    @staticmethod
    def execute_command(command: str, extra):
        '''Executes a given command'''
        if not Commands.__INITIALIZED:
            return "I'm sorry. I seem to be unable to process your instruction this moment."

        location = extra if ('WEATHER' in command or 'TIME' in command) else None
        app = extra if 'APP' in command else None

        # Time

        if 'TIME_CURRENT' in command:
            return DateTime.get_time(location)

        if 'DATE_CURRENT' in command:
            return DateTime.get_date()

        if 'DAY_CURRENT' in command:
            return DateTime.get_day()

        # Weather

        if 'CURRENT_WEATHER' in command:
            return Weather.get_current_weather_overview(location)

        if 'CURRENT_TEMP' in command:
            return Weather.get_current_weather_specific('temperature', location)

        if 'CURRENT_HUMIDITY' in command:
            return Weather.get_current_weather_specific('humidity', location)

        if 'CURRENT_CLOUD' in command:
            return Weather.get_current_weather_specific('clouds', location)

        if 'CURRENT_PRECIP' in command:
            return Weather.get_current_weather_specific('precip', location)

        if 'CURRENT_WIND' in command:
            return Weather.get_current_weather_specific('windspeed', location)

        if 'FORECAST_TOMORROW' in command:
            return Weather.get_weather_forecast_tomorrow(location)

        if 'FORECAST_TODAY' in command:
            return Weather.get_weather_forecast_today(location)

        if 'RAIN_TOMORROW' in command:
            return Weather.get_rain(location, 'tomorrow')

        if 'RAIN_TODAY' in command:
            return Weather.get_rain(location, 'today')

        if 'TEMP_TOMORROW' in command:
            return Weather.get_temp(location, 'tomorrow')

        if 'TEMP_TODAY' in command:
            return Weather.get_temp(location, 'today')

        # Quotes
        if 'QUOTE_INSPIRATIONAL' in command:
            return Quoter.inspire()

        # Music
        if 'MUSIC_STUDY' in command:
            return MusicPlayer.play_study_music()

        if 'MUSIC_STOP' in command:
            return MusicPlayer.stop_music()

        # Apps
        if 'APP_OPEN' in command:
            return Appy.open_app(app)

        if 'APP_CLOSE' in command:
            return Appy.close_app(app)

        # Search
        if 'SEARCH_PROMPT' in command:
            return LookUp.search(extra)

        return Commands.commands['DEFAULT_RESPONSE']
