import speech_recognition

class Listener:
    
    @staticmethod
    def listen_for(keywords: list, responses: list):
        
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