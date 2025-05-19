from fastapi import FastAPI
from fastapi_mcp import FastApiMCP
import uvicorn


app = FastAPI()

@app.get("/items/{item_id}", operation_id="read_item")
async def read_item(item_id: int):
    return {"item_id": item_id, "name": f"Item {item_id}"}

mcp = FastApiMCP(app,
                 name="READ ITEM APP",
                 description="FastAPI example with MCP",
                 describe_all_responses=True,     # Include all possible response schemas in tool descriptions
                describe_full_response_schema=True) # Include full JSON schema in tool descriptions)

mcp.mount()

def main():
   uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()