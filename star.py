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

# Create MCP server - FastMCP likely returns the server object directly
def create_mcp_server():
    client = httpx.AsyncClient()
    # FastMCP.from_fastapi likely returns an ASGI-compatible object directly
    mcp = FastMCP.from_fastapi(
        app, 
        client,
        transport="http-streamable"
    )
    # Return the FastMCPOpenAPI object directly - it should be ASGI compatible
    return mcp

# Alternative approach - create a simple FastAPI app for MCP if the above doesn't work
def create_simple_mcp_app():
    mcp_app = FastAPI(title="MCP Server")
    
    @mcp_app.get("/")
    async def mcp_root():
        return {"message": "MCP Server is running"}
    
    @mcp_app.get("/health")
    async def mcp_health():
        return {"status": "healthy"}
    
    return mcp_app

# Try to create MCP server, fallback to simple app if it fails
try:
    mcp_server = create_mcp_server()
except Exception as e:
    print(f"Failed to create MCP server: {e}")
    print("Using simple MCP app instead")
    mcp_server = create_simple_mcp_app()

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