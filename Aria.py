'''Main runnable for Aria, containing the Aria object-class'''

from random import choice
import json
from Body.mouth import TTSModule
from Body.brain import Commands
from Body.ears import Listener
from Skills.conversation import Conversation
from Utilities.command_line import CmdLine

class Aria:
    '''Aria object-class'''

    def __init__(self) -> None:
        self.speaker = TTSModule()
        Commands.init()
        CmdLine.outputln("...")

    def run(self):
        '''Aria's main running method'''

        # Begin listening loop
        while True:
            # Wait to be called
            convo_type = Listener.listen_for(['chat', 'aria'], ['chat', 'task'])

            # Chat or perform tasks
            if convo_type == 'task':
                instruction = self.do_tasks()
            elif convo_type == 'chat':
                instruction = self.chat()

            # Shut down completely
            if instruction == 'go to sleep':
                break

    def do_tasks(self):
        '''Task Mode'''

        self.__introduce()

        # Begin instruction loop
        while True:
            instruction = Listener.listen()

            if instruction in ['nevermind', 'go to sleep']:
                self.speaker.speak("Okay. Let me know when you need anything else.")
                return instruction

            # Understand instruction
            command, xtra = Commands.parse_command(instruction)

            # Error catch command
            if command is None:
                self.speaker.speak("I'm sorry. I seem to be unable to \
                                    process your instruction this moment.")
                continue

            # Perform task
            self.speaker.speak(Commands.execute_command(command, xtra))

    def chat(self):
        '''Chat Mode'''

        self.__introduce()

        conversation = Conversation()

        while True:
            message = Listener.listen()

            if message in ['nevermind', 'go to sleep']:
                self.speaker.speak("Okay. Let me know when you need anything else.")
                return message

            reply = conversation.get_response(message)
            self.speaker.speak(reply)

    def __introduce(self):
        '''Lets user know she is listening'''
        with open('./data/conversationSettings.json', encoding='UTF-8') as settings:
            message = json.load(settings)['default_replies']
            self.speaker.speak(choice(message))

if __name__ == '__main__':
    aria = Aria()
    aria.run()
