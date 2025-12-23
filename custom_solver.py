from util import Util
from time import sleep
from curl_cffi import requests
import json

config = Util.get_config()

SOLVER_KEY = config.get("solverKey", "")
API_URL = "https://api.funbypass.com"


def get_token(roblox_session: requests.Session, blob, proxy):
    session = requests.Session()

    task_payload = {
        "clientKey": SOLVER_KEY,
        "task": {
            "type": "FunCaptchaTask",
            "websiteURL": "https://www.roblox.com/",
            "websitePublicKey": "A2A14B1D-1AF3-C791-9BBC-EE33CC7A0A6F",
            "websiteSubdomain": "roblox.com",
            "data": json.dumps({"blob": blob}),
            "proxy": proxy,
        },
    }

    create_resp = session.post(f"{API_URL}/createTask", json=task_payload, timeout=60)
    if create_resp.status_code != 200:
        raise ValueError(f"createTask HTTP {create_resp.status_code}: {create_resp.text}")
    create_data = create_resp.json()
    if create_data.get("errorId") != 0:
        raise ValueError(f"createTask error: {create_data}")
    task_id = create_data.get("taskId")
    if not task_id:
        raise ValueError(f"createTask missing taskId: {create_data}")

    for _ in range(60):
        sleep(1)
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
