'''Aria's text-to-speech functionality'''

import os
from gtts import gTTS
from playsound import playsound
from Utilities.command_line import CmdLine

class TTSModule:
    '''Object class which allows for speaking'''

    def __init__(self):
        self.__fname = 'speech.mp3'

    def speak(self, words: str):
        '''Speaks text aloud'''

        CmdLine.outputln('...')

        try:
            speech = gTTS(words, tld='ca', lang='en')
            speech.save(self.__fname)
        except Exception:
            CmdLine.outputln(f"{words}\n\n\
                Something has gone wrong with my voice module!\n\
                Are you connected to the internet?")
            os.remove(self.__fname)
            return

        CmdLine.outputln(words)
        playsound(self.__fname)
        os.remove(self.__fname)
