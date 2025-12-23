from threading import Lock
from counter import counter
from output import Output
from session import Session
from auth_intent import AuthIntent
from util import Util
from custom_solver import get_token
from json import loads, dumps
from base64 import b64encode, b64decode

LOCK = Lock()


class GroupJoiner:
    @staticmethod
    def join_group(group_id: str, cookie: str, stop_event) -> None:
        try:
            Output("INFO").log(f"Attempting to join group {group_id}")

            session = Session.session()
            
            # Set cookie
            session.cookies.set('.ROBLOSECURITY', cookie, domain='.roblox.com')

            # Get CSRF token - use a lightweight endpoint
            resp = session.post("https://auth.roblox.com/v2/logout")
            
            if resp.status_code == 429:
                raise ValueError("Rate limited")

            csrf = resp.headers.get("x-csrf-token")
            
            if csrf:
                session.headers = {
                    **session.headers,
                    "x-csrf-token": csrf
                }

            session.headers = Session.set_api_request_headers(session.headers)
            session.headers = Util.sort_dict_order(session.headers)

            # Attempt to join group
            resp = session.post(f"https://groups.roblox.com/v1/groups/{group_id}/users")

            if resp.status_code == 429:
                raise ValueError("Rate limited")

            if resp.status_code == 200:
                counter.increment()
                Output("SUCCESS").log(f"Successfully joined group {group_id}")
                
                with LOCK:
                    with open("output/joined_groups.txt", "a", encoding="utf-8") as file:
                        file.write(f"{group_id}|{cookie[:50]}...\n")
                return

            # Handle captcha challenge
            if resp.status_code == 403:
                challenge_id = resp.headers.get("rblx-challenge-id")
                
                if not challenge_id:
                    raise ValueError("Failed to join group - Forbidden (No captcha challenge)")
                
                metadata = loads(b64decode(resp.headers.get(
                    "rblx-challenge-metadata").encode("utf-8")).decode("utf-8"))
                blob = metadata.get("dataExchangeBlob")
                captcha_id = metadata.get("unifiedCaptchaId")

                Output("CAPTCHA").log("Solving captcha")

                # Get proxy from session
                proxy = None
                if hasattr(session, 'proxy'):
                    proxy = session.proxy
                elif hasattr(session, 'proxies') and session.proxies:
                    proxy = session.proxies.get('http') or session.proxies.get('https')
                
                solution = get_token(session, blob, proxy)

                if solution == None:
                    raise ValueError("Failed to solve captcha")

                token = solution.split("|")[0]
                token_info = solution.split(
                    "pk=A2A14B1D-1AF3-C791-9BBC-EE33CC7A0A6F|")[1].split("|cdn_url=")[0]

                Output("CAPTCHA").log(f"Solved captcha | {token}|{token_info}")

                challenge_metadata = dumps({
                    "unifiedCaptchaId": captcha_id,
                    "captchaToken": solution,
                    "actionType": "GroupJoin"
                }, separators=(',', ':'))

                payload = dumps({
                    "challengeId": challenge_id,
                    "challengeType": "captcha",
                    "challengeMetadata": challenge_metadata
                }, separators=(',', ':'))

                resp = session.post(
                    "https://apis.roblox.com/challenge/v1/continue", content=payload.encode("utf-8"))

                if resp.status_code != 200:
                    raise ValueError("Rejected by continue API")

                session.headers = {
                    **session.headers,
                    "rblx-challenge-id": challenge_id,
                    "rblx-challenge-metadata": b64encode(challenge_metadata.encode("utf-8")).decode("utf-8"),
                    "rblx-challenge-type": "captcha"
                }

                session.headers = Util.sort_dict_order(session.headers)

                # Retry joining group with captcha solution
                resp = session.post(f"https://groups.roblox.com/v1/groups/{group_id}/users")

                if resp.status_code != 200:
                    raise ValueError(f"Rejected by group join API - Status: {resp.status_code}")

                counter.increment()
                Output("SUCCESS").log(f"Successfully joined group {group_id}")
                
                with LOCK:
                    with open("output/joined_groups.txt", "a", encoding="utf-8") as file:
                        file.write(f"{group_id}|{cookie[:50]}...\n")
                return
            
            # Handle other status codes
            raise ValueError(f"Unexpected response status: {resp.status_code}")

        except Exception as e:
            if "Failed to perform" in str(e):
                Output("ERROR").log("Error | Proxy failed to make request")
            else:
                Output("ERROR").log(f"Error | {str(e)}")
