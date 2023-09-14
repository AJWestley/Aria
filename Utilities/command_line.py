'''Useful command line printing tools'''

import os

class CmdLine:

    @staticmethod
    def clear_terminal():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def output(text: str):
        CmdLine.clear_terminal()
        print(text, end=' ')

    @staticmethod
    def outputln(text: str):
        CmdLine.clear_terminal()
        print(text, end='\n\n')
