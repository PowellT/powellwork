# Install required packages
# pip install fastmcp fastapi uvicorn

from fastapi import FastAPI, HTTPException
from fastmcp import FastMCP, Context
from pydantic import BaseModel
from typing import Optional, List
import asyncio
import threading
import uvicorn

# Shared data models
class User(BaseModel):
    id: int
    name: str
    email: str

class Task(BaseModel):
    id: int
    title: str
    completed: bool = False
    user_id: int

# Shared data store (in production, use a real database)
users_db = {
    1: {"id": 1, "name": "Alice", "email": "alice@example.com"},
    2: {"id": 2, "name": "Bob", "email": "bob@example.com"}
}

tasks_db = {
    1: {"id": 1, "title": "Complete project", "completed": False, "user_id": 1},
    2: {"id": 2, "title": "Review code", "completed": True, "user_id": 1},
    3: {"id": 3, "title": "Write documentation", "completed": False, "user_id": 2}
}

# === FastAPI Application ===
fastapi_app = FastAPI(title="Task Management API", version="1.0.0")

@fastapi_app.get("/users/{user_id}", response_model=User)
def get_user_api(user_id: int):
    """Get user by ID via REST API"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return users_db[user_id]

@fastapi_app.get("/tasks", response_model=List[Task])
def get_tasks_api():
    """Get all tasks via REST API"""
    return list(tasks_db.values())

@fastapi_app.post("/tasks", response_model=Task)
def create_task_api(task: Task):
    """Create a new task via REST API"""
    tasks_db[task.id] = task.dict()
    return task

# === MCP Server Application ===
mcp = FastMCP("Task Management MCP Server")

@mcp.tool()
async def create_user_task(user_id: int, title: str, ctx: Context) -> dict:
    """Create a new task for a specific user via MCP"""
    await ctx.info(f"Creating task '{title}' for user {user_id}")
    
    if user_id not in users_db:
        return {"error": "User not found"}
    
    # Generate new task ID
    new_id = max(tasks_db.keys()) + 1 if tasks_db else 1
    
    task = {
        "id": new_id,
        "title": title,
        "completed": False,
        "user_id": user_id
    }
    
    tasks_db[new_id] = task
    await ctx.info(f"Task {new_id} created successfully")
    return task

@mcp.tool()
async def complete_task(task_id: int, ctx: Context) -> dict:
    """Mark a task as completed via MCP"""
    await ctx.info(f"Marking task {task_id} as completed")
    
    if task_id not in tasks_db:
        return {"error": "Task not found"}
    
    tasks_db[task_id]["completed"] = True
    await ctx.info(f"Task {task_id} marked as completed")
    return tasks_db[task_id]

@mcp.tool()
def get_user_stats(user_id: int) -> dict:
    """Get task statistics for a user via MCP"""
    if user_id not in users_db:
        return {"error": "User not found"}
    
    user_tasks = [task for task in tasks_db.values() if task["user_id"] == user_id]
    completed_tasks = [task for task in user_tasks if task["completed"]]
    
    return {
        "user_id": user_id,
        "user_name": users_db[user_id]["name"],
        "total_tasks": len(user_tasks),
        "completed_tasks": len(completed_tasks),
        "completion_rate": len(completed_tasks) / len(user_tasks) if user_tasks else 0
    }

@mcp.resource("user://{user_id}")
def get_user_resource(user_id: str) -> dict:
    """Get user information as MCP resource"""
    user_id_int = int(user_id)
    if user_id_int not in users_db:
        return {"error": "User not found"}
    return users_db[user_id_int]

@mcp.resource("tasks://all")
def get_all_tasks_resource() -> List[dict]:
    """Get all tasks as MCP resource"""
    return list(tasks_db.values())

@mcp.resource("tasks://user/{user_id}")
def get_user_tasks_resource(user_id: str) -> List[dict]:
    """Get tasks for a specific user as MCP resource"""
    user_id_int = int(user_id)
    return [task for task in tasks_db.values() if task["user_id"] == user_id_int]

@mcp.prompt()
def task_summary_prompt(user_id: int) -> str:
    """Generate a prompt for task summary analysis"""
    user_tasks = [task for task in tasks_db.values() if task["user_id"] == user_id]
    completed = len([t for t in user_tasks if t["completed"]])
    total = len(user_tasks)
    
    return f"""Analyze the following task data for user {user_id}:
    
Total tasks: {total}
Completed tasks: {completed}
Pending tasks: {total - completed}

Task details: {user_tasks}

Please provide insights about the user's productivity and suggest improvements."""

# === Application Runner ===
class AppRunner:
    def __init__(self):
        self.fastapi_thread = None
        
    def run_fastapi_server(self):
        """Run FastAPI server in a separate thread"""
        uvicorn.run(fastapi_app, host="127.0.0.1", port=8000, log_level="info")
    
    def start_fastapi(self):
        """Start FastAPI in background thread"""
        self.fastapi_thread = threading.Thread(target=self.run_fastapi_server)
        self.fastapi_thread.daemon = True
        self.fastapi_thread.start()
        print("✅ FastAPI server started on http://127.0.0.1:8000")
        print("   - REST API endpoints available")
        print("   - OpenAPI docs at http://127.0.0.1:8000/docs")
    
    def run_mcp_server(self):
        """Run MCP server for AI agent integration"""
        print("✅ MCP server starting...")
        print("   - Tools and resources available for AI agents")
        mcp.run()
    
    def run_combined(self):
        """Run both FastAPI and MCP servers"""
        self.start_fastapi()
        print("\n" + "="*50)
        print("COMBINED SERVER MODE")
        print("="*50)
        print("FastAPI (REST): http://127.0.0.1:8000")
        print("MCP Server: Available for AI agent connections")
        print("="*50 + "\n")
        
        # Run MCP server in main thread
        self.run_mcp_server()

# === CLI Interface ===
if __name__ == "__main__":
    import sys
    
    runner = AppRunner()
    
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
        if mode == "fastapi":
            print("Running FastAPI server only...")
            runner.run_fastapi_server()
        elif mode == "mcp":
            print("Running MCP server only...")
            runner.run_mcp_server()
        elif mode == "combined":
            print("Running combined FastAPI + MCP servers...")
            runner.run_combined()
        else:
            print("Usage: python script.py [fastapi|mcp|combined]")
            sys.exit(1)
    else:
        # Default: run combined mode
        print("Running in combined mode (default)...")
        runner.run_combined()