from fastapi import FastAPI
from fastmcp import FastMCP
import httpx
import uvicorn

# Your FastAPI app (keeps Swagger at /docs)
app = FastAPI()

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    return {"user_id": user_id, "name": "John Doe"}

# Run FastAPI normally
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)  # Swagger available at http://localhost:8000/docs

# Separately, create MCP server for AI agents
async def create_mcp_server():
    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        mcp_server = FastMCP.from_fastapi(app, client)
        return mcp_server