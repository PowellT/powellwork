#!/usr/bin/env python3
"""
Simple MCP Server using FastMCP
This server provides basic tools and resources for demonstration.
"""

import asyncio
from typing import Any, Dict, List
from fastmcp import FastMCP

# Initialize the FastMCP server
mcp = FastMCP("Simple MCP Server")

@mcp.tool()
def add_numbers(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b

@mcp.tool()
def greet(name: str) -> str:
    """Greet someone by name."""
    return f"Hello, {name}! Welcome to the MCP server."

@mcp.tool()
def get_system_info() -> Dict[str, Any]:
    """Get basic system information."""
    import platform
    import os
    
    return {
        "platform": platform.system(),
        "python_version": platform.python_version(),
        "current_directory": os.getcwd(),
        "environment_variables_count": len(os.environ)
    }

@mcp.resource("file://example.txt")
def get_example_file() -> str:
    """Provide sample text content."""
    return """This is an example text file served by the MCP server.
It contains some sample content that can be accessed as a resource.

You can modify this content or add more resources as needed."""

@mcp.resource("config://server-info")
def get_server_info() -> Dict[str, Any]:
    """Provide information about this MCP server."""
    return {
        "name": "Simple MCP Server",
        "version": "1.0.0",
        "description": "A basic MCP server demonstration",
        "tools_available": ["add_numbers", "greet", "get_system_info"],
        "resources_available": ["file://example.txt", "config://server-info"]
    }

async def main():
    """Run the MCP server."""
    # Get the server instance
    server = mcp.create_server()
    
    # Run the server
    await server.run()

if __name__ == "__main__":
    asyncio.run(main())