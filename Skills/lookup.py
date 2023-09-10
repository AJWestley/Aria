import webbrowser

class LookUp:
    
    __triggers = ["search", "look up", "lookup", "google"]
    
    @staticmethod
    def search(prompt: str):
        query = "+".join(prompt.split(' '))
        url = f"https://www.google.com/search?q={query}"
        webbrowser.open(url)
        return f"Here's what I found on Google for '{prompt}'."
    
    @staticmethod
    def get_triggers():
        return LookUp.__triggers