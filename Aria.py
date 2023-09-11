from Body.mouth import TTS_Module
from Body.brain import Commands
from Body.ears import Listener
from Skills.conversation import Conversation
from Utilities.command_line import CmdLine

class Aria:
    def __init__(self) -> None:
        # Init TTS
        self.speaker = TTS_Module()
        CmdLine.outputln("...")

    def run(self):

        # Begin listening loop
        while True:
            
            # Wait to be called
            convo_type = Listener.listen_for(['chat', 'aria'], ['chat', 'task'])
            self.speaker.speak("I'm listening...")

            # Chat or perform tasks
            if convo_type == 'task':
                instruction = self.do_tasks()
            elif convo_type == 'chat':
                instruction = self.chat()
                
            # Shut down completely
            if instruction == 'go to sleep':
                break
        
    def do_tasks(self):
        # Begin instruction loop
            while True:
                instruction = Listener.listen()

                if instruction in ['nevermind', 'go to sleep']:
                    self.speaker.speak("Okay. Let me know when you need anything else")
                    return instruction
                
                # Understand instruction
                command, xtra = Commands.parse_command(instruction)
                
                # Perform task
                self.speaker.speak(Commands.execute_command(command, xtra))
        
    def chat(self):
        conversation = Conversation()
        
        while True:
            message = Listener.listen()
            
            if message in ['nevermind', 'go to sleep']:
                self.speaker.speak("Okay. Let me know when you need anything else")
                return message
            
            reply = conversation.get_response(message)
            self.speaker.speak(reply)
        
if __name__ == '__main__':
    aria = Aria()
    aria.run()