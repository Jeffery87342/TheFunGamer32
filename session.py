try:
    from curl_cffi.requests import Session as CurlSession
    USE_CURL_CFFI = True
except ImportError:
    import requests
    USE_CURL_CFFI = False

from util import Util

class Session:
    @staticmethod
    def session():
        browsers = [
            ("chrome136", '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"', "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36")
        ]

        browser = browsers[0]
        proxy = Util.get_random_proxy()

        if USE_CURL_CFFI:
            session = CurlSession(
                impersonate="chrome_133",
                proxy=proxy,
                verify=False
            )
        else:
            session = requests.Session()
            if proxy:
                session.proxies = {'http': proxy, 'https': proxy}
            session.verify = False

        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-encoding': 'gzip, deflate, br, zstd',
            'accept-language': f'{Util.get_random_string()};q=0.9,en;q=0.8',
            'content-type': 'application/json;charset=UTF-8',
            'origin': 'https://www.roblox.com',
            'priority': 'u=0, i',
            'sec-ch-ua': browser[1],
            'sec-ch-ua-mobile': "?0",
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': "document",
            'sec-fetch-user': "?1",
            'sec-fetch-mode': "navigate",
            'sec-fetch-site': "same-origin",
            'user-agent': browser[2],
            'upgrade-insecure-requests': '1'
        }

        session.headers = Util.sort_dict_order(headers)
        if USE_CURL_CFFI and proxy:
            session.proxy = proxy

        return session

    @staticmethod
    def set_page_request_headers(headers: dict) -> dict:
        headers.update({
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'priority': 'u=0, i',
            'sec-fetch-dest': 'document',
            'sec-fetch-user': '?1',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'upgrade-insecure-requests': '1'
        })

        return Util.sort_dict_order(headers)

    @staticmethod
    def set_api_request_headers(headers: dict) -> dict:
        headers.pop('upgrade-insecure-requests', None)
        headers.pop('sec-fetch-user', None)

        headers.update({
            'accept': 'application/json, text/plain, */*',
            'priority': 'u=1, i',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site'
        })

        return Util.sort_dict_order(headers)
