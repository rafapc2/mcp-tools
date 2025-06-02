import time

# Simulación del token cache y expiración
token_cache = {
    "access_token": None,
    "expires_at": 0  # timestamp en segundos
}

EXPIRY_BUFFER = 60  # segundos antes de expiración para refrescar

# Función para generar un token simulado
async def fetch_token():
    # Simula el tiempo actual y vencimiento
    current_time = int(time.time())
    token_cache["access_token"] = "dummy-access-token"
    token_cache["expires_at"] = current_time + 3600 - EXPIRY_BUFFER  # simula 1 hora de validez

    return token_cache["access_token"]

# Devuelve el token si no ha expirado, o lo renueva
async def get_token():
    now = int(time.time())
    if token_cache["access_token"] is None or now >= token_cache["expires_at"]:
        return await fetch_token()
    return token_cache["access_token"]
