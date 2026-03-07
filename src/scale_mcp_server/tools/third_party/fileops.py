"""Filesystem MCP Tools - Third-party integration tools.

This module contains the actual @mcp.tool() decorated functions that are registered
with the FastMCP server. These tools proxy requests to the external filesystem MCP server.
"""

from typing import Any
from fastmcp import FastMCP
from scale_mcp_server.adapters.fileops import get_fileops_client


# Create the file operations MCP server
mcp = FastMCP(
    "fileops",
    instructions="File and directory operations via external MCP server"
)


@mcp.tool()
async def read_file(path: str) -> str:
    """Read the complete contents of a file from the filesystem.

    Args:
        path: The path to the file to read

    Returns:
        The contents of the file as a string
    """
    client = await get_fileops_client()
    result = await client.call_tool("read_file", {"path": path})
    return str(result)


@mcp.tool()
async def read_multiple_files(paths: list[str]) -> str:
    """Read the contents of multiple files simultaneously.

    Args:
        paths: List of file paths to read

    Returns:
        Combined contents of all files
    """
    client = await get_fileops_client()
    result = await client.call_tool("read_multiple_files", {"paths": paths})
    return str(result)


@mcp.tool()
async def write_file(path: str, content: str) -> str:
    """Create a new file or overwrite an existing file with new content.

    Args:
        path: The path where the file should be written
        content: The content to write to the file

    Returns:
        Success message
    """
    client = await get_fileops_client()
    result = await client.call_tool("write_file", {"path": path, "content": content})
    return str(result)


@mcp.tool()
async def edit_file(
    path: str, edits: list[dict[str, Any]], dryRun: bool = False
) -> str:
    """Make line-based edits to a text file.

    Args:
        path: The path to the file to edit
        edits: List of edit operations
        dryRun: If true, show what would be done without applying changes

    Returns:
        Result of the edit operation
    """
    client = await get_fileops_client()
    result = await client.call_tool(
        "edit_file", {"path": path, "edits": edits, "dryRun": dryRun}
    )
    return str(result)


@mcp.tool()
async def create_directory(path: str) -> str:
    """Create a new directory or ensure a directory exists.

    Args:
        path: The path of the directory to create

    Returns:
        Success message
    """
    client = await get_fileops_client()
    result = await client.call_tool("create_directory", {"path": path})
    return str(result)


@mcp.tool()
async def list_directory(path: str) -> str:
    """Get a detailed listing of all files and directories in a specified path.

    Args:
        path: The path of the directory to list

    Returns:
        Detailed directory listing
    """
    client = await get_fileops_client()
    result = await client.call_tool("list_directory", {"path": path})
    return str(result)


@mcp.tool()
async def directory_tree(path: str) -> str:
    """Get a recursive tree view of files and directories.

    Args:
        path: The root path to start the tree from

    Returns:
        Tree structure of the directory
    """
    client = await get_fileops_client()
    result = await client.call_tool("directory_tree", {"path": path})
    return str(result)


@mcp.tool()
async def move_file(source: str, destination: str) -> str:
    """Move or rename files and directories.

    Args:
        source: The source path
        destination: The destination path

    Returns:
        Success message
    """
    client = await get_fileops_client()
    result = await client.call_tool(
        "move_file", {"source": source, "destination": destination}
    )
    return str(result)


@mcp.tool()
async def search_files(
    path: str, pattern: str, excludePatterns: list[str] | None = None
) -> str:
    """Recursively search for files and directories matching a pattern.

    Args:
        path: The root path to search from
        pattern: The search pattern (glob format)
        excludePatterns: Optional list of patterns to exclude

    Returns:
        List of matching paths
    """
    client = await get_fileops_client()
    params = {"path": path, "pattern": pattern}
    if excludePatterns:
        params["excludePatterns"] = excludePatterns
    result = await client.call_tool("search_files", params)
    return str(result)


@mcp.tool()
async def get_file_info(path: str) -> str:
    """Retrieve detailed metadata about a file or directory.

    Args:
        path: The path to get information about

    Returns:
        Detailed file/directory information
    """
    client = await get_fileops_client()
    result = await client.call_tool("get_file_info", params={"path": path})
    return str(result)


@mcp.tool()
async def list_allowed_directories() -> str:
    """Get a list of directories that this server is allowed to access.

    Returns:
        List of allowed directory paths
    """
    client = await get_fileops_client()
    result = await client.call_tool("list_allowed_directories", {})
    return str(result)
