'''Installation file for Aria'''

import os
import json

def create_key_file():
    '''Creates API key file with default content'''
    fpath = './data/keys.json'
    if os.path.exists(fpath):
        return
    keys = json.dumps({"WEATHER_API_KEY": "key here", "OPEN_AI_KEY": "key here"})
    with open(fpath, 'w', encoding='ascii') as keyfile:
        keyfile.write(keys)


def install():
    '''Installs requirements'''
    os.system("pip install -r requirements.txt")

if __name__ == "__main__":
    install()
    create_key_file()
