try:
    from curl_cffi.requests import Session as CurlSession
    USE_CURL_CFFI = True
except ImportError:
    import requests
    USE_CURL_CFFI = False

from util import Util
from time import sleep
import json

config = Util.get_config()

SOLVER_KEY = config.get("solverKey", "")
API_URL = "https://api.funbypass.com"


def get_token(roblox_session, blob, proxy):
    """
    Solve FunCaptcha using FunBypass.com API
    
    Args:
        roblox_session: The Roblox session (not used directly, kept for compatibility)
        blob: The captcha blob from Roblox challenge
        proxy: Proxy string in format: protocol://username:password@host:port
               Supported protocols: http, https, socks4, socks5
    
    Returns:
        Captcha solution token or None if failed
    """
    if USE_CURL_CFFI:
        session = CurlSession()
    else:
        session = requests.Session()

    task_payload = {
        "clientKey": SOLVER_KEY,
        "task": {
            "type": "FunCaptchaTask",
            "websiteURL": "https://www.roblox.com/",
            "websitePublicKey": "476068BF-9607-4799-B53D-966BE98E2B81",
            "websiteSubdomain": "arkoselabs.roblox.com",
            "data": json.dumps({"blob": blob}),
            "proxy": proxy,
        },
    }

    # Step 1: Create captcha solving task
    create_resp = session.post(f"{API_URL}/createTask", json=task_payload, timeout=60)
    if create_resp.status_code != 200:
        raise ValueError(f"createTask HTTP {create_resp.status_code}: {create_resp.text}")
    create_data = create_resp.json()
    if create_data.get("errorId") != 0:
        raise ValueError(f"createTask error: {create_data}")
    task_id = create_data.get("taskId")
    if not task_id:
        raise ValueError(f"createTask missing taskId: {create_data}")

    # Step 2: Poll for solution (120 iterations with 0.5s sleep = 60 seconds max)
    for _ in range(120):
        sleep(0.5)
        result_resp = session.get(f"{API_URL}/getTaskResult/{task_id}", timeout=30)
        if result_resp.status_code not in (200, 202):
            continue
        result_data = result_resp.json()
        if result_data.get("errorId") != 0:
            raise ValueError(f"getTaskResult error: {result_data}")
        status = result_data.get("status")
        if status == "processing":
            continue
        if status == "ready":
            solution = result_data.get("solution")
            if isinstance(solution, dict) and "token" in solution:
                return solution["token"]
            if isinstance(solution, str):
                return solution
            return None
        if status == "failure":
            return None

    return None
