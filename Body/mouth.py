from gtts import gTTS
from playsound import playsound
from Utilities.command_line import CmdLine
import os

class TTS_Module:
    
    def __init__(self):
        self.volume = 0.5
    
    def speak(self, words: str):
        CmdLine.outputln('...')
        fname = 'speech.mp3'
        speech = gTTS(words, tld='ca', lang='en')
        speech.save(fname)
        CmdLine.outputln(words)
        playsound(fname)
        os.remove(fname)