import logging
from fastapi import FastAPI
from fastapi_mcp import FastApiMCP
import uvicorn
from auth import fetch_token, get_token
import httpx
from contextlib import asynccontextmanager

logging.basicConfig(level=logging.DEBUG)
LOG = logging.getLogger("foo")
LOG.debug("Iniciando el script")

app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    LOG.info("Obteniendo token OAuth2 al iniciar...")
    await fetch_token()
    LOG.info("Token OAuth2 obtenido correctamente")
    
    yield  # Aquí arranca el servidor

    LOG.info("Apagando aplicación...")  # Opcional para shutdown


app = FastAPI(lifespan=lifespan)

@app.get("/items/{item_id}", operation_id="read_item")
async def read_item(item_id: int, q: str | None = None):
    token = await get_token()

    if q:
        LOG.debug("llamada desde sesion q=%s", q)
    match item_id:
        case 1:
            item_detail = "Knife set"
        case 2:
            item_detail = "Spoons set"
        case _:
            item_detail = "fork set"

    # Simulamos una llamada saliente autenticada
    async with httpx.AsyncClient() as client:
        headers = {"Authorization": f"Bearer {token}"}
        # Ejemplo de llamada real:
        # response = await client.get("https://api.ejemplo.com/datos", headers=headers)
        # data = response.json()

    return {"item_id": item_id, "name": f"Detail {item_detail}"}

mcp = FastApiMCP(
    app,
    name="READ ITEM APP",
    description="FastAPI example with MCP and OAuth2 token refresh",
    describe_all_responses=True,
    describe_full_response_schema=True
)

mcp.mount()

def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
