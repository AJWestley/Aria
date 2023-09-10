from random import choice

def introduction():
    intros = [
        "Hello, I'm Arya, your AI assistant here to help you.",
        "Greetings! I'm Arya, your digital companion at your service.",
        "Hi there, I'm Arya, your virtual assistant ready to assist you.",
        "Welcome! I'm Arya, the AI designed to make your life easier.",
    ]
    return choice(intros)

