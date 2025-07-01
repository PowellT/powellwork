#!/usr/bin/env python3
"""
Simple MCP Server using FastMCP with Uvicorn
This server provides basic tools and resources for demonstration.
"""

import os
import platform
from typing import Any, Dict
from fastmcp import FastMCP

# Initialize the FastMCP server
mcp = FastMCP("Simple MCP Server")

@mcp.tool()
def add_numbers(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b

@mcp.tool()
def multiply_numbers(a: float, b: float) -> float:
    """Multiply two numbers together."""
    return a * b

@mcp.tool()
def greet(name: str) -> str:
    """Greet someone by name."""
    return f"Hello, {name}! Welcome to the MCP server."

@mcp.tool()
def get_system_info() -> Dict[str, Any]:
    """Get basic system information."""
    return {
        "platform": platform.system(),
        "platform_release": platform.release(),
        "platform_version": platform.version(),
        "architecture": platform.machine(),
        "processor": platform.processor(),
        "python_version": platform.python_version(),
        "current_directory": os.getcwd(),
        "environment_variables_count": len(os.environ)
    }

@mcp.tool()
def reverse_string(text: str) -> str:
    """Reverse a given string."""
    return text[::-1]

@mcp.resource("file://example.txt")
def get_example_file() -> str:
    """Provide sample text content."""
    return """This is an example text file served by the MCP server.
It contains some sample content that can be accessed as a resource.

This server is running with uvicorn and provides several tools:
- Mathematical operations (add, multiply)
- String manipulation (reverse)
- System information retrieval
- Greeting functionality

You can modify this content or add more resources as needed."""

@mcp.resource("config://server-info")
def get_server_info() -> Dict[str, Any]:
    """Provide information about this MCP server."""
    return {
        "name": "Simple MCP Server",
        "version": "1.0.0",
        "description": "A basic MCP server running with uvicorn",
        "server": "uvicorn",
        "tools_available": [
            "add_numbers", 
            "multiply_numbers", 
            "greet", 
            "get_system_info", 
            "reverse_string"
        ],
        "resources_available": [
            "file://example.txt", 
            "config://server-info"
        ]
    }

@mcp.resource("data://sample-data")
def get_sample_data() -> Dict[str, Any]:
    """Provide some sample data."""
    return {
        "users": [
            {"id": 1, "name": "Alice", "role": "admin"},
            {"id": 2, "name": "Bob", "role": "user"},
            {"id": 3, "name": "Charlie", "role": "user"}
        ],
        "settings": {
            "theme": "dark",
            "notifications": True,
            "auto_save": False
        }
    }

# Create the ASGI app
app = mcp.create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)