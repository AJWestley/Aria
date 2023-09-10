import speech_recognition

class Listener:
    
    @staticmethod
    def listen_for(keyword: str):
        
        ear = speech_recognition.Recognizer()
        
        while True:
            
            try:
                with speech_recognition.Microphone(device_index=0) as mic:
                    ear.adjust_for_ambient_noise(mic, duration=0.2)
                    audio = ear.listen(mic)
                    text = ear.recognize_google(audio).lower()
                    if keyword in text: break
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