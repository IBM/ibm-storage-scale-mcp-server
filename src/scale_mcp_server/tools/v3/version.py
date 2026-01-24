"""IBM Storage Scale Version Management MCP Server."""

from typing import Optional, Any
from fastmcp import FastMCP, Context
from scale_mcp_server.api.v3.version import get_version_api

# Create the version MCP server
mcp = FastMCP("version", instructions="Version information operations")


@mcp.tool()
async def get_version(
    ctx: Context,
    domain: Optional[str] = None,
) -> Any:
    """Get IBM Storage Scale version information.

    Args:
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing version information
    """
    await ctx.info("Tool called: get_version")
    await ctx.debug("Retrieving IBM Storage Scale version information")

    try:
        result = await get_version_api(domain=domain)
        await ctx.info("Successfully retrieved version information")
        return result
    except Exception as e:
        await ctx.error(f"Failed to get version: {str(e)}")
        raise
