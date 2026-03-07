"""File Operations MCP Server Integration for IBM Storage Scale MCP Server.

This module provides integration with the MCP filesystem server (https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem),
managing the client connection and initialization.
"""

from fastmcp.client import Client
from fastmcp.client.transports.stdio import StdioTransport


# Global client instance that will be initialized when the server starts
_fileops_client: Client | None = None
_client_connected: bool = False


async def get_fileops_client() -> Client:
    """Get the file operations client instance, connecting it if needed.
    
    The client must be used within an async context manager.
    This function ensures the client is connected before returning it.
    """
    global _fileops_client, _client_connected
    
    if _fileops_client is None:
        raise RuntimeError(
            "File operations client not initialized. Call initialize_fileops_client first."
        )
    
    # Connect the client if not already connected
    if not _client_connected:
        await _fileops_client.__aenter__()
        _client_connected = True
    
    return _fileops_client


def initialize_fileops_client(allowed_paths: list[str]) -> None:
    """Initialize the file operations client connection.

    This creates a Client connection to the external MCP filesystem server.
    The connection will be established on first tool use.
    
    Note: The fileops client ALWAYS uses StdioTransport regardless of how
    the main server is configured. This is because it connects to an external
    Node.js-based MCP server (@modelcontextprotocol/server-filesystem) that
    only supports stdio transport. The main server's transport (stdio/http)
    only affects how clients connect to THIS server, not how this server
    connects to external MCP servers.

    Args:
        allowed_paths: List of allowed directory paths for file operations
    """
    global _fileops_client, _client_connected

    # Create the transport for the filesystem server
    # Note: Always uses stdio because the external filesystem server is a
    # separate Node.js process launched via npx that only supports stdio
    transport = StdioTransport(
        command="npx",
        args=["-y", "@modelcontextprotocol/server-filesystem"] + allowed_paths,
    )

    # Create the client (connection happens on first tool call via get_fileops_client)
    _fileops_client = Client(transport)
    _client_connected = False
