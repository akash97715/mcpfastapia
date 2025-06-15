from fastapi import FastAPI
from fastapi_mcp import FastApiMCP

app = FastAPI(
    title="My MCP API",
    description="A sample MCP-compatible FastAPI server",
    version="1.0.0"
)

from fastapi import Path


from fastapi import Request
import logging

@app.middleware("http")
async def log_request(request: Request, call_next):
    body = await request.body()
    logging.info(f"Request body: {body.decode('utf-8')}")
    response = await call_next(request)
    return response


@app.get("/items/{item_id}", operation_id="get_item")
async def get_item(item_id: int):
    return {"item_id": item_id, "name": f"Item {item_id}"}

@app.get("/routes")
async def get_routes():
    return [{"path": route.path, "methods": list(route.methods)} for route in app.routes]


# Mount MCP **after** all routes
mcp = FastApiMCP(
    app,
    "My API MCP",
    "MCP server for my API",
    "http://localhost:8000"
)
mcp.mount()

# Start the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
