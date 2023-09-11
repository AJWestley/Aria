import openai
import json

class Conversation:
    def __init__(self):
        self.reset()
        openai.api_key = json.load(open('./data/keys.json'))['OPEN_AI_KEY']
        
    def get_response(self, prompt: str):
        try:
            self.messages.append({'role': 'user', 'content': prompt})
            completion = openai.ChatCompletion.create(
                model=self.model, 
                messages=self.messages, 
                temperature=self.temperature, 
                max_tokens=self.max_tokens
            )
            self.messages.append(completion.choices[0]['message'])
            return completion.choices[0]['message']['content']
        except Exception:
            return "I'm sorry, I don't understand."
        
    def reset(self):
        data = json.load(open('./data/conversationSettings.json'))
        self.messages = data['settings']
        self.model = data['model']
        self.temperature = data['temperature']
        self.max_tokens = data['max_tokens']
        
if __name__ == '__main__':
    chat = Conversation()
    print(chat.get_response("Whats your name"))