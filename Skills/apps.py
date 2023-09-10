from AppOpener import open, close

class Appy:
    
    @staticmethod
    def open_app(app_name: str):
        open(app_name, match_closest=True, output=False)
        return f"Opening {app_name}."

    @staticmethod
    def close_app(app_name: str):
        close(app_name, match_closest=True, output=False)
        return f"Closing {app_name}."
    
