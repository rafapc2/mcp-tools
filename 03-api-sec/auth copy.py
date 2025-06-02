import httpx
import os
import time
from dotenv import load_dotenv

load_dotenv()

TOKEN_URL = os.getenv("OAUTH2_TOKEN_URL")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
SCOPE = os.getenv("SCOPE", "read")

# Token cache
token_cache = {
    "access_token": None,
    "expires_at": 0  # timestamp en segundos
}

# Buffer de tiempo antes de que expire (en segundos)
EXPIRY_BUFFER = 60

async def fetch_token():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            TOKEN_URL,
            data={
                "grant_type": "client_credentials",
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "scope": SCOPE,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        response.raise_for_status()
        token_data = response.json()

        expires_in = token_data.get("expires_in", 3600)  # valor por defecto: 1 hora
        expires_at = int(time.time()) + expires_in - EXPIRY_BUFFER

        token_cache["access_token"] = token_data["access_token"]
        token_cache["expires_at"] = expires_at

        return token_cache["access_token"]

async def get_token():
    now = int(time.time())
    if token_cache["access_token"] is None or now >= token_cache["expires_at"]:
        return await fetch_token()
    return token_cache["access_token"]
