"""IBM Storage Scale Diagnostics MCP Server."""

from typing import Optional, Any
from fastmcp import FastMCP, Context
from scale_mcp_server.api.v3.diagnostics import get_node_version_api

# Create the diagnostics MCP server
mcp = FastMCP("diagnostics", instructions="Diagnostics operations")


@mcp.tool()
async def get_node_version(
    ctx: Context,
    node: str,
    domain: Optional[str] = None,
) -> Any:
    """Get version information for a specific node.

    Args:
        node: Node name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing node version information
    """
    await ctx.info(f"Tool called: get_node_version with node={node}")
    await ctx.debug(f"Retrieving version information for node: {node}")

    try:
        result = await get_node_version_api(node=node, domain=domain)
        await ctx.info(f"Successfully retrieved version for node: {node}")
        return result
    except Exception as e:
        await ctx.error(f"Failed to get node version for {node}: {str(e)}")
        raise
