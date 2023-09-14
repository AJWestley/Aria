'''Open/Close local apps'''

from AppOpener import open as aopen, close as aclose

class Appy:

    @staticmethod
    def open_app(app_name: str):
        aopen(app_name, match_closest=True, output=False)
        return f"Opening {app_name}."

    @staticmethod
    def close_app(app_name: str):
        aclose(app_name, match_closest=True, output=False)
        return f"Closing {app_name}."
