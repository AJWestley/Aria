'''Have a conversation with Aria, powered by OpenAI chat completion'''

import json
import openai

class Conversation:
    '''Object-class containing the ongoing conversation'''

    def __init__(self):
        '''Constructs the conversation with the necessary settings'''
        self.reset()
        with open('./data/keys.json', encoding='UTF-8') as keys:
            openai.api_key = json.load(keys)['OPEN_AI_KEY']

    def get_response(self, prompt: str):
        '''Sends a message to the assistant and gets the response'''
        try:
            self.messages.append({'role': 'user', 'content': prompt})
            completion = openai.ChatCompletion.create(
                model=self.model,
                messages=self.messages,
                max_tokens=self.max_tokens
            )
            self.messages.append(completion.choices[0]['message'])
            return completion.choices[0]['message']['content']
        except Exception:
            return "I'm sorry, I don't understand."

    def reset(self):
        '''Clears all messages and sets settings back to default'''
        with open('./data/conversationSettings.json', encoding='UTF-8') as settings:
            data = json.load(settings)
            self.messages = data['settings']
            self.model = data['model']
            self.temperature = data['temperature']
            self.max_tokens = data['max_tokens']

if __name__ == '__main__':
    chat = Conversation()
    print(chat.get_response("Whats your name"))
