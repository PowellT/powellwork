# Install required packages
# pip install fastmcp fastapi uvicorn

from fastapi import FastAPI
from fastmcp import FastMCP
from pydantic import BaseModel
from typing import Optional

# Your existing FastAPI application
fastapi_app = FastAPI(title="My Existing API", version="1.0.0")

# FastAPI Models
class Item(BaseModel):
    name: str
    price: float
    description: Optional[str] = None

class User(BaseModel):
    id: int
    name: str
    email: str

# Your existing FastAPI endpoints
@fastapi_app.get("/status")
def get_status():
    """Get the current system status"""
    return {"status": "running", "version": "1.0.0"}

@fastapi_app.get("/users/{user_id}")
def get_user(user_id: int):
    """Get user information by ID"""
    # Mock data - replace with your actual logic
    return {"id": user_id, "name": f"User {user_id}", "email": f"user{user_id}@example.com"}

@fastapi_app.post("/items")
def create_item(item: Item):
    """Create a new item"""
    # Mock creation - replace with your actual logic
    return {"id": 1, "name": item.name, "price": item.price, "description": item.description}

@fastapi_app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    """Update an existing item"""
    return {"id": item_id, "name": item.name, "price": item.price, "description": item.description}

@fastapi_app.delete("/items/{item_id}")
def delete_item(item_id: int):
    """Delete an item"""
    return {"message": f"Item {item_id} deleted successfully"}

# Generate MCP server from FastAPI app
# This automatically converts:
# - GET requests -> MCP resources
# - GET requests with path parameters -> MCP resource templates  
# - All other HTTP methods (POST, PUT, DELETE) -> MCP tools
mcp_server = FastMCP.from_fastapi(fastapi_app)

# Option 1: Run as MCP server
def run_mcp_server():
    """Run the MCP server for AI agent integration"""
    mcp_server.run()

# Option 2: Run FastAPI normally
def run_fastapi():
    """Run the FastAPI server normally"""
    import uvicorn
    uvicorn.run(fastapi_app, host="127.0.0.1", port=8000)

# Option 3: Run both simultaneously (different ports)
def run_both():
    """Run both FastAPI and MCP servers"""
    import threading
    import uvicorn
    
    # Run FastAPI in a separate thread
    fastapi_thread = threading.Thread(
        target=lambda: uvicorn.run(fastapi_app, host="127.0.0.1", port=8000)
    )
    fastapi_thread.daemon = True
    fastapi_thread.start()
    
    print("FastAPI running on http://127.0.0.1:8000")
    print("MCP server starting...")
    
    # Run MCP server in main thread
    mcp_server.run()

if __name__ == "__main__":
    # Choose your approach:
    # run_mcp_server()  # For AI agent integration
    # run_fastapi()     # For normal web API
    run_both()          # For both simultaneously