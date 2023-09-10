from Utilities.attempt_request import attempt_request
from random import choice

class Quoter:
    __BASE_URL = "https://zenquotes.io/api"

    __DEF_QUOTES = [
        "It always seems impossible until it's done. - Nelson Mandela", 
        "Life is what you make it. Always has been, always will be. - Eleanor Roosevelt",
        "The secret of life isn't what happens to you, but what you do with what happens to you. - Norman Vincent Peale",
        "You must live in the present, launch yourself on every wave, find your eternity in each moment. Fools stand on their island of opportunities and look toward another land. There is no other land; there is no other life but this. - Henry David Thoreau",
        "It is during our darkest moments that we must focus to see the light. - Aristotle",
        "Don't gain the world and lose your soul. Wisdom is better than silver and gold. - Bob Marley",
        "Everything has its beauty, but not everyone sees it.  - Confucius",
        "You can easily judge the character of a man by how he treats those who can do nothing for him. - Simon Sinek",
        "If you're not making mistakes, then you're not doing anything. - John Wooden",
        "Incredible change happens in your life when you decide to take control of what you do have power over instead of craving control over what you don't. - Steve Maraboli"
    ]

    @staticmethod
    def inspire() -> str:
        
        url = f"{Quoter.__BASE_URL}/random"
        response = attempt_request(url)
        
        # Could not make request (Internet issue?)
        if response is None:
            return "I'm sorry, something went wrong. Are you sure your internet is working properly?"
        
        # Received error code
        if response.status_code != 200:
            return choice(Quoter.__DEF_QUOTES)
        
        quote = response.json()[0]
        
        return f"Here's an inspirational quote for you by {quote['a']}:\n\n'{quote['q']}'"