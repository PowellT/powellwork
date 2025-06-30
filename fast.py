from fastapi import FastAPI
from fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.routing import Mount
import httpx
import uvicorn

# Your FastAPI app
app = FastAPI(title="My API")

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    return {"user_id": user_id, "name": "John Doe"}

@app.post("/users")
async def create_user(name: str):
    return {"message": f"User {name} created"}

# Create MCP server - Note: This needs to be handled properly for async context
# You may need to adjust this based on FastMCP's actual implementation
def create_mcp_server():
    client = httpx.AsyncClient()
    return FastMCP.from_fastapi(
        app, 
        client,
        transport="http-streamable"  # Specify transport
    )

mcp_server = create_mcp_server()

# Mount both applications
main_app = Starlette(routes=[
    Mount("/api", app),      # FastAPI with Swagger at /api/docs
    Mount("/mcp", mcp_server),  # MCP server at /mcp
])

if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",  # Replace "main" with your actual filename
        host="0.0.0.0",
        port=8000,
        reload=True
    )