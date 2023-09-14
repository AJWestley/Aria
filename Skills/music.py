'''Aria's music playing functionality'''

import webbrowser
import os

class MusicPlayer:

    @staticmethod
    def play_study_music():
        '''Plays a Lofi study stream from YouTube'''
        webbrowser.open("https://www.youtube.com/watch?v=jfKfPfyJRdk", autoraise=False, new=1)
        return "Playing your study music."

    @staticmethod
    def stop_music():
        '''Closes Spotify and Chrome to stop music'''
        os.system("taskkill /f /im chrome.exe")
        os.system("taskkill /f /im spotify.exe")
        return "Stopping music."

