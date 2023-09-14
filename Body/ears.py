'''Aria's speech-recognition'''

import speech_recognition

class Listener:
    '''Static class with useful speech-recognition functions'''

    @staticmethod
    def listen_for(keywords: list, responses: list):
        '''
        Listens until a given word is said 
        and returns the necessary response
        '''

        if len(keywords) != len(responses):
            responses = [None for _ in keywords]
        replies = dict(zip(keywords, responses))

        ear = speech_recognition.Recognizer()

        while True:

            try:
                with speech_recognition.Microphone(device_index=0) as mic:
                    ear.adjust_for_ambient_noise(mic, duration=0.2)
                    audio = ear.listen(mic)
                    text = ear.recognize_google(audio).lower()

                    for keyword in replies:
                        if keyword in text:
                            return replies[keyword]

            except Exception:
                ear = speech_recognition.Recognizer()
                continue

    @staticmethod
    def listen():
        '''Listens and returns everything heard'''

        ear = speech_recognition.Recognizer()

        while True:

            try:
                with speech_recognition.Microphone(device_index=0) as mic:
                    ear.adjust_for_ambient_noise(mic, duration=0.2)
                    audio = ear.listen(mic)
                    if text := ear.recognize_google(audio).lower():
                        return text
            except Exception:
                ear = speech_recognition.Recognizer()
                continue
