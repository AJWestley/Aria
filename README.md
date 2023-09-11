<h1 align="center">✨ Aria ✨</h1>
<p align="center">An AI personal assistant I designed to make my life easier.</p>

## About Aria

### What can she do?

Aria can perform a variety of tasks. These tasks include:
- Date and Time:
  - Tell you the date
  - Tell you the time (locally or in a specific place)
 
- Weather:
  - Current weather conditions (locally or in a specific place)
  - Weather forecasts for today or tomorrow (locally or in a specific place)
 
- Quotes:
  - Generate inspirational quotes
 
- Music:
  - Play lofi study music
  - Stop music
 
- Apps:
  - Open and close apps
 
- Web Search:
  - Google things for you  

- Chat:
  - She can chat with you, using GPT 3.5 Turbo

### Chatting to Aria

- #### Conversation Modes

  Aria has 2 conversation modes: *task mode* and *chat mode*. 

  - ***Task Mode*** </br>
    To enter task mode with Aria, you need to call her first! </br>
    To call Aria, simply say ***"Aria"*** in any sentence and she will start listening for instructions.

  - ***Chat Mode*** </br>
    If you want to chat with Aria, just say ***"chat"*** in a sentence. </br>
    I personally prefer to say "Let's chat"!

  If you use both keywords, Aria will enter chat mode.

- #### Ending a conversation
  If you want to end a conversation with Aria, just say ***"nevermind"***. </br>
  This will leave whatever mode she is in, but she'll still be listening for you to call her again!

- #### Putting Aria to sleep
  Another way you can end a conversation is by saying ***"Go to sleep"***. </br>
  This will shut Aria down completely. She won't listen for you to call her again.

- #### Searching the web
  To search the web, you must use ***"Google"***, ***"Search"***, or ***"Look up"*** in a sentence. </br>
  This will open a Google tab where the rest your sentence is used as the search prompt.

## Getting Started

### API Keys

Some of Arias functionality relies external APIs. 
In order to use them, you will need to generate your own API keys and add them to *keys.json*.

```json
{
  "WEATHER_API_KEY": "key here",
  "OPEN_AI_KEY": "key here"
}
```

The *WEATHER_API_KEY* can be created for free <a href="https://www.weatherapi.com">here</a>. </br>
The *OPEN_AI_KEY* can be created <a href="https://platform.openai.com">here</a> but you must buy credits before the chat feature can be used.

### Dependencies

Before running Aria, make sure all the necessary dependencies are installed. 
This can be done with the _install.py_ script.

```bash
# python can be used in place of python3 in some cases
python3 install.py      
```

**Take Note:** One of the dependencies is a NLP text-similarity module which needs about 600mb to install.

### Potential Issues

#### The playsound Module

Some new versions of the playsound module are not compatible with Aria's text-to-speech module. 
A the *requirements.txt* has a compatible version, but if your device already has playsound installed, the compatible installation may be skipped. 
The issue can be fixed in two ways: </br></br>

- **Option 1: Changing your playsound version** </br>
  You can change your current python environment's playsound version with the following code:

  ```bash
  pip uninstall playsound
  pip install playsound==1.2.2
  ```

- **Option 2: Running Aria inside a virtual environment** </br>
  Option 1 could affect any modules or files on your device which depend on the playsound module.
  If you don't want these files to be affected, you could rather make use of a virtual environment. </br>
  - First <a href="https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/">setup a virtual environment</a>. </br>
  - Once that's done, run the install script from within the environment.

## Plans for Aria

### On the way:
- Altering system settings
- Telling you about anstronomy conditions

### Potential Ideas:
- Integrating other OpenAI features (DALL-E?)
- YouTube searching/downloading
- Changing terminal output to match voice volume
