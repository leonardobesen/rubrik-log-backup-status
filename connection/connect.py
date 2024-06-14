import json
import requests
from configuration.configuration import load_config
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

CONNECTION_CONFIG = None


def open_session() -> str:
    global CONNECTION_CONFIG

    if not CONNECTION_CONFIG:
        CONNECTION_CONFIG = load_config()

    headers = {'Content-Type': 'application/json'}

    data = json.dumps({
        'client_id': CONNECTION_CONFIG["client_id"],
        'client_secret': CONNECTION_CONFIG["client_secret"]
    })

    access_token = requests.post(CONNECTION_CONFIG["access_token_uri"],
                                 data=data,
                                 headers=headers,
                                 verify=False)

    if access_token.status_code != 200:
        raise (ValueError(
            f"Response failed with error code {access_token.status_code}: \n{access_token.text}"))

    return access_token.json()["access_token"]


def close_session(access_token: str):
    global CONNECTION_CONFIG

    if not CONNECTION_CONFIG:
        CONNECTION_CONFIG = load_config()

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    requests.delete(
        CONNECTION_CONFIG["access_token_uri"], headers=headers, verify=False)
