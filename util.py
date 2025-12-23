from string import digits, ascii_letters
from random import choice, randint
from json import load
import os

def load_proxies():
    # Check for proxies.txt in root directory first, then input directory
    proxy_files = ["proxies.txt", "input/proxies.txt"]
    
    for proxy_file in proxy_files:
        if os.path.exists(proxy_file):
            with open(proxy_file, "r", encoding="utf-8") as file:
                proxies = [line.strip() for line in file.readlines() if line.strip()]
                if proxies:
                    return proxies
    return []

def load_config():
    config_file = "input/config.json"
    if os.path.exists(config_file):
        with open(config_file, "r", encoding="utf-8") as file:
            return load(file)
    return {}

proxies = load_proxies()
config = load_config()

class Util:
    @staticmethod
    def get_random_proxy() -> str:
        if proxies:
            proxy = choice(proxies).strip()
            # Ensure proxy has http:// prefix
            if not proxy.startswith('http://') and not proxy.startswith('https://'):
                proxy = f'http://{proxy}'
            return proxy
        return None
    
    @staticmethod
    def get_config() -> dict:
        return config
    
    @staticmethod
    def get_random_string() -> str:
        return ''.join([choice(ascii_letters + digits) for _ in range(randint(12, 20))])
    
    @staticmethod
    def sort_dict_order(input_dict: dict) -> dict:
        keys_order = [
            'sec-ch-ua-platform',
            'upgrade-insecure-requests',
            'x-csrf-token',
            'user-agent',
            'accept',
            'sec-ch-ua',
            'content-type',
            'sec-ch-ua-mobile',
            'origin',
            'sec-fetch-site',
            'sec-fetch-mode',
            'sec-fetch-dest',
            'referer',
            'accept-encoding',
            'accept-language',
            'cookie',
            'priority'
        ]

        ordered_dict = {key: input_dict[key] for key in keys_order if key in input_dict}

        remaining_keys = {key: value for key, value in input_dict.items() if key not in keys_order}
        ordered_dict.update(remaining_keys)

        return ordered_dict
