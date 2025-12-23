from datetime import datetime
from colorama import init, Fore
from threading import Lock

init()

lock = Lock()

class Output:
    def __init__(self, level):
        self.level = level
        self.color_map = {
            "INFO": (Fore.LIGHTBLUE_EX, "^"),
            "CAPTCHA": (Fore.WHITE, "🤖"),
            "ERROR": (Fore.LIGHTRED_EX, "❌"),
            "SUCCESS": (Fore.LIGHTGREEN_EX, "✅"),
            "GROUP": (Fore.MAGENTA, "👥"),
        }

    def log(self, *args, **kwargs):
        color, text = self.color_map.get(self.level, (Fore.RESET, "INFO"))
        time_now = datetime.now().strftime("%H:%M:%S")

        base = f"{Fore.LIGHTBLACK_EX}[{time_now}]{Fore.RESET} ({color}{text.upper()}{Fore.RESET})"
        for arg in args:
            base += f"{color} {arg}"
        if kwargs:
            base += f"{color} {arg}"
        with lock:
            print(base)
