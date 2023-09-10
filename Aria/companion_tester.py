from tts import TTS_Module
from commands import Commands
import listener

speaker = TTS_Module()

while True:
    listener.listen_for('aria')
    speaker.speak("I'm listening...")
    while True:
        i = listener.listen()
        if 'nevermind' in i or 'sleep' in i:
            speaker.speak("Okay. Let me know when you need anything else")
            break
        command, xtra = Commands.parse_command(i)
        speaker.speak(Commands.execute_command(command, xtra))
    if 'sleep' in i:
        break