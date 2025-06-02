import logging
from fastapi import FastAPI
from fastapi_mcp import FastApiMCP
import uvicorn


logging.basicConfig(level=logging.DEBUG) 
LOG = logging.getLogger("foo")
LOG.debug("Iniciando el script")

app = FastAPI()

@app.get("/user/{user_id}", operation_id="get_user_data")
async def get_user_data(user_id: int, q: str | None = None):

    if q:
        LOG.debug("llamada desde sesion q=%s", q)
    match user_id:
        case 1:
            LOG.debug("llamada desde sesion item_id=1")
            item_detail = "Rafael Prudencio"
        case 2:
            LOG.debug("llamada desde sesion item_id=2")
            item_detail = "Adriano Lopez"
        case _:
            LOG.debug("llamada desde sesion item_id=%s", user_id)
            item_detail = "Joaquin de la Vega"

    return {"item_id": user_id, "name": f"Detail {item_detail}"}

mcp = FastApiMCP(app,
                name="banking_user_data_api",
                description="User data API for banking operations",
                describe_all_responses=True,     # Include all possible response schemas in tool descriptions
                describe_full_response_schema=True) # Include full JSON schema in tool descriptions

mcp.mount()

def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
