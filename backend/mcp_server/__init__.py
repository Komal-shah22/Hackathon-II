"""MCP Server initialization and tool registration."""
from fastmcp import FastMCP

# 1. Create MCP server instance FIRST (before any imports from tools.py)
mcp_server = FastMCP("todo-mcp-server")

# 2. NOW import the registration function (after server exists)
from .tools import register_all_mcp_tools

# 3. Register all tools with the server
register_all_mcp_tools(mcp_server)

# 4. Export for use in other modules
__all__ = ["mcp_server"]