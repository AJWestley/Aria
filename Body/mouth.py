from gtts import gTTS
from playsound import playsound
from Utilities.command_line import CmdLine
import os

class TTS_Module:
    
    def __init__(self):
        pass
    
    def speak(self, words: str):
        
        CmdLine.outputln('...')
        fname = 'speech.mp3'
        
        try:
            speech = gTTS(words, tld='ca', lang='en')
            speech.save(fname)
        except Exception:
            CmdLine.outputln(f"{words}\n\nSomething has gone wrong with my voice module!\nAre you connected to the internet?")
            os.remove(fname)
            return
        
        CmdLine.outputln(words)
        playsound(fname)
        os.remove(fname)