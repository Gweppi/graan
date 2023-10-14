""" main """
import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_access_token(username: str, password: str) -> str:
    """ Function obtaining access token """
    data = {
        "client_id": "cdse-public",
        "username": username,
        "password": password,
        "grant_type": "password",
    }
    try:
        r = requests.post(
            "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token",
            data=data,
            timeout=10
        )
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        raise Exception(f"Access token creation failed. Response from the server was: {r.json()}") from e
    return r.json()["access_token"]

usernameEnv = os.environ.get("USERNAME")
passwordEnv = os.environ.get("PASSWORD")

access_token = get_access_token(usernameEnv, passwordEnv)

print(access_token)
