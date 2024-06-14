import requests
from configuration.configuration import load_config
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Global Variable for GraphQL URL
GRAPHQL_URL = None


def request(access_token: str, query: str, variables=None) -> dict:
    global GRAPHQL_URL

    if not GRAPHQL_URL:
        GRAPHQL_URL = load_config()["graphql_url"]

    base_url = GRAPHQL_URL
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    if not variables:
        response = requests.post(
            base_url, json={'query': query}, headers=headers, verify=False)
    else:
        response = requests.post(base_url, json={
                                 'query': query, 'variables': variables}, headers=headers, verify=False)

    if response.status_code != 200:
        raise ValueError(
            f"Response failed with error code {response.status_code}: \n{response.text}")

    return response.json()
