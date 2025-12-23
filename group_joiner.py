from threading import Lock
from counter import counter
from output import Output
from session import Session
from auth_intent import AuthIntent
from util import Util
from custom_solver import get_token
from json import loads, dumps
from base64 import b64encode, b64decode
import os

LOCK = Lock()


class GroupJoiner:
    @staticmethod
    def join_group(group_id: str, cookie: str, stop_event) -> None:
        try:
            Output("INFO").log(f"Attempting to join group {group_id}")

            session = Session.session()
            
            # Set cookie for authentication
            session.cookies.set('.ROBLOSECURITY', cookie, domain='.roblox.com')

            # Step 1: Get CSRF token by making a request that will fail but return the token
            # Using the logout endpoint is the standard way to get CSRF token
            session.headers = Session.set_api_request_headers(session.headers)
            session.headers = Util.sort_dict_order(session.headers)
            
            Output("INFO").log("Fetching CSRF token...")
            resp = session.post("https://auth.roblox.com/v2/logout")
            
            if resp.status_code == 429:
                raise ValueError("Rate limited - Need more proxies or slower rate")

            csrf = resp.headers.get("x-csrf-token")
            
            if not csrf:
                # Try alternative method - make any POST request to trigger CSRF token return
                resp = session.post("https://groups.roblox.com/v1/groups/{group_id}/users")
                csrf = resp.headers.get("x-csrf-token")
            
            if csrf:
                session.headers["x-csrf-token"] = csrf
                session.headers = Util.sort_dict_order(session.headers)
                Output("INFO").log(f"CSRF token acquired: {csrf[:20]}...")
            else:
                raise ValueError("Failed to acquire CSRF token")

            # Step 2: Attempt to join group
            Output("INFO").log(f"Sending join request to group {group_id}...")
            resp = session.post(f"https://groups.roblox.com/v1/groups/{group_id}/users")

            if resp.status_code == 429:
                raise ValueError("Rate limited - Need more proxies or slower rate")

            # Success - joined without captcha
            if resp.status_code == 200:
                counter.increment()
                Output("SUCCESS").log(f"Successfully joined group {group_id}")
                
                # Create output directory if it doesn't exist
                os.makedirs("output", exist_ok=True)
                with LOCK:
                    with open("output/joined_groups.txt", "a", encoding="utf-8") as file:
                        file.write(f"{group_id}|{cookie[:50]}...\n")
                return

            # Handle captcha challenge (403 with challenge headers)
            if resp.status_code == 403 or resp.headers.get("rblx-challenge-id"):
                challenge_id = resp.headers.get("rblx-challenge-id")
                
                if not challenge_id:
                    raise ValueError(f"Failed to join group - Forbidden (Status: {resp.status_code}, No captcha challenge)")
                
                challenge_metadata_b64 = resp.headers.get("rblx-challenge-metadata")
                if not challenge_metadata_b64:
                    raise ValueError("Captcha challenge received but no metadata")
                
                try:
                    metadata = loads(b64decode(challenge_metadata_b64.encode("utf-8")).decode("utf-8"))
                except Exception as e:
                    raise ValueError(f"Failed to decode challenge metadata: {e}")
                
                Output("CAPTCHA").log(f"Challenge metadata: {metadata}")
                
                blob = metadata.get("dataExchangeBlob")
                captcha_id = metadata.get("unifiedCaptchaId")
                challenge_type_from_metadata = metadata.get("challengeType", "captcha")
                
                # Check for newer challenge format with sessionId and genericChallengeId
                session_id = metadata.get("sessionId")
                generic_challenge_id = metadata.get("sharedParameters", {}).get("genericChallengeId") if isinstance(metadata.get("sharedParameters"), dict) else None
                
                if not blob and session_id and generic_challenge_id:
                    # This is a newer Roblox challenge format that doesn't use FunCaptcha
                    Output("INFO").log(f"Detected newer challenge format with sessionId: {session_id}")
                    Output("INFO").log(f"Generic challenge ID: {generic_challenge_id}")
                    
                    # Try to continue with the generic challenge
                    # Build redemption metadata
                    redemption_metadata = {
                        "sessionId": session_id,
                        "redemptionToken": metadata.get("redemptionToken", "")
                    }
                    
                    continue_payload = dumps({
                        "challengeId": challenge_id,
                        "challengeType": "generic",
                        "challengeMetadata": b64encode(dumps(redemption_metadata).encode("utf-8")).decode("utf-8")
                    }, separators=(',', ':'))
                    
                    Output("INFO").log("Attempting to continue with generic challenge...")
                    resp = session.post(
                        "https://apis.roblox.com/challenge/v1/continue", 
                        content=continue_payload.encode("utf-8")
                    )
                    
                    if resp.status_code == 200:
                        Output("SUCCESS").log("Generic challenge accepted")
                        # Add challenge headers to session
                        session.headers.update({
                            "rblx-challenge-id": challenge_id,
                            "rblx-challenge-metadata": challenge_metadata_b64,
                            "rblx-challenge-type": "generic"
                        })
                        
                        # Retry the group join with challenge headers
                        Output("INFO").log("Retrying group join with challenge headers...")
                        resp = session.post(f"https://groups.roblox.com/v1/groups/{group_id}/users")
                        
                        if resp.status_code == 200:
                            counter.increment()
                            Output("SUCCESS").log(f"Successfully joined group {group_id}")
                            os.makedirs("output", exist_ok=True)
                            with LOCK:
                                with open("output/joined_groups.txt", "a", encoding="utf-8") as file:
                                    file.write(f"{group_id}|{cookie[:50]}...\n")
                            return
                        else:
                            Output("ERROR").log(f"Group join failed after challenge: Status {resp.status_code}, Body: {resp.text[:200]}")
                            raise ValueError(f"Failed to join group after generic challenge: {resp.status_code}")
                    else:
                        Output("ERROR").log(f"Generic challenge continue failed: Status {resp.status_code}, Body: {resp.text[:200]}")
                        raise ValueError(f"Failed to continue generic challenge: {resp.status_code}")

                if not blob:
                    # No blob and not a generic challenge - unknown challenge type
                    Output("ERROR").log(f"Unknown challenge format. Metadata: {metadata}")
                    raise ValueError(f"No captcha blob and unrecognized challenge format. Challenge type: {challenge_type_from_metadata}")

                Output("CAPTCHA").log(f"Captcha challenge detected (ID: {captcha_id})")

                # Get proxy from session for captcha solver
                proxy = None
                if hasattr(session, 'proxy'):
                    proxy = session.proxy
                elif hasattr(session, 'proxies') and session.proxies:
                    proxy = session.proxies.get('http') or session.proxies.get('https')
                
                if not proxy:
                    Output("CAPTCHA").log("⚠️  No proxy available - captcha solving may fail")
                else:
                    Output("CAPTCHA").log(f"Using proxy for captcha: {proxy[:30]}...")

                # Solve captcha using FunBypass
                Output("CAPTCHA").log("Sending to FunBypass.com for solving...")
                solution = get_token(session, blob, proxy)

                if solution == None:
                    raise ValueError("Failed to solve captcha - FunBypass returned no solution")

                Output("CAPTCHA").log(f"Captcha solved! Token: {solution[:50]}...")

                # Prepare challenge response
                challenge_metadata = dumps({
                    "unifiedCaptchaId": captcha_id,
                    "captchaToken": solution,
                    "actionType": "GroupJoin"
                }, separators=(',', ':'))

                continue_payload = dumps({
                    "challengeId": challenge_id,
                    "challengeType": "captcha",
                    "challengeMetadata": challenge_metadata
                }, separators=(',', ':'))

                # Submit captcha solution to Roblox
                Output("CAPTCHA").log("Submitting captcha solution to Roblox...")
                resp = session.post(
                    "https://apis.roblox.com/challenge/v1/continue", 
                    content=continue_payload.encode("utf-8")
                )

                if resp.status_code != 200:
                    raise ValueError(f"Captcha continue API rejected solution - Status: {resp.status_code}")

                # Add challenge headers for retry
                session.headers["rblx-challenge-id"] = challenge_id
                session.headers["rblx-challenge-metadata"] = b64encode(challenge_metadata.encode("utf-8")).decode("utf-8")
                session.headers["rblx-challenge-type"] = "captcha"
                session.headers = Util.sort_dict_order(session.headers)

                # Retry joining group with captcha solution
                Output("CAPTCHA").log("Retrying group join with captcha solution...")
                resp = session.post(f"https://groups.roblox.com/v1/groups/{group_id}/users")

                if resp.status_code == 200:
                    counter.increment()
                    Output("SUCCESS").log(f"Successfully joined group {group_id} (with captcha)")
                    
                    os.makedirs("output", exist_ok=True)
                    with LOCK:
                        with open("output/joined_groups.txt", "a", encoding="utf-8") as file:
                            file.write(f"{group_id}|{cookie[:50]}...\n")
                    return
                else:
                    raise ValueError(f"Group join failed after captcha - Status: {resp.status_code}, Response: {resp.text[:100]}")
            
            # Handle other status codes
            raise ValueError(f"Unexpected response - Status: {resp.status_code}, Response: {resp.text[:200]}")

        except Exception as e:
            error_msg = str(e)
            if "Failed to perform" in error_msg or "ProxyError" in error_msg or "ConnectionError" in error_msg:
                Output("ERROR").log("Error | Proxy failed to make request")
            elif "Rate limited" in error_msg:
                Output("ERROR").log(f"Error | {error_msg}")
            else:
                Output("ERROR").log(f"Error | {error_msg}")
