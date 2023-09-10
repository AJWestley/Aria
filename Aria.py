from Body.mouth import TTS_Module
from Body.brain import Commands
from Body.ears import Listener
from Skills.casual_conversation import introduction
import os

def main():
    
    # Init TTS & greet user
    speaker = TTS_Module()
    speaker.speak(introduction())

    # Begin listening loop
    while True:
        
        # Wait to be called
        Listener.listen_for('aria')
        speaker.speak("I'm listening...")

        # Begin conversation loop
        while True:
            
            # Listen to instruction
            instruction = Listener.listen()

            # Check for conversation end
            if instruction in ['nevermind', 'go to sleep']:
                speaker.speak("Okay. Let me know when you need anything else")
                break
            
            # Understand instruction
            command, xtra = Commands.parse_command(instruction)
            
            # Perform task
            speaker.speak(Commands.execute_command(command, xtra))
            
        # Shut down completely
        if instruction == 'go to sleep':
            break
        
if __name__ == '__main__':
    main()