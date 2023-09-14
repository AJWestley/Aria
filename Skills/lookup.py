'''Aria's web-surfing functionality'''

import webbrowser

class LookUp:
    __triggers = ["search", "look up", "lookup", "google"]

    @staticmethod
    def search(prompt: str):
        '''Search google for a given prompt'''
        query = "+".join(prompt.split(' '))
        url = f"https://www.google.com/search?q={query}"
        webbrowser.open(url)
        return f"Here's what I found on Google for '{prompt}'."

    @staticmethod
    def get_triggers():
        '''Gets Aria's search trigger words'''
        return LookUp.__triggers
