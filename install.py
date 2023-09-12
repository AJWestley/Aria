import os
import json

def create_key_file():
    fpath = './data/keys.json'
    if os.path.exists(fpath):
        return
    keys = json.dump({"WEATHER_API_KEY": "key here", "OPEN_AI_KEY": "key here"})
    with open(fpath, 'w') as keyfile:
        keyfile.write(keys)
    

def install():
    os.system("pip install -r requirements.txt")
    
if __name__ == "__main__":
    install()
    create_key_file()