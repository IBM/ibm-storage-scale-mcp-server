"""IBM Storage Scale Node Management MCP Server."""

from typing import Optional, Any
from fastmcp import FastMCP, Context
from scale_mcp_server.api.v3.nodes import (
    get_nodes_config_api,
    get_nodes_status_api,
    start_nodes_api,
    stop_nodes_api,
)

# Create the nodes MCP server
mcp = FastMCP("nodes", instructions="Node management operations")


@mcp.tool()
async def get_nodes_config(
    ctx: Context,
    domain: Optional[str] = None,
) -> Any:
    """Get configuration of all nodes.

    Args:
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing nodes configuration
    """
    await ctx.info("Tool called: get_nodes_config")
    await ctx.debug("Retrieving configuration for all nodes")

    try:
        result = await get_nodes_config_api(domain)
        await ctx.info("Successfully retrieved nodes configuration")
        return result
    except Exception as e:
        await ctx.error(f"Failed to get nodes config: {str(e)}")
        raise


@mcp.tool()
async def get_nodes_status(
    ctx: Context,
    domain: Optional[str] = None,
) -> Any:
    """Get status of all nodes.

    Args:
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing nodes status
    """
    await ctx.info("Tool called: get_nodes_status")
    await ctx.debug("Retrieving status for all nodes")

    try:
        result = await get_nodes_status_api(domain)
        await ctx.info("Successfully retrieved nodes status")
        return result
    except Exception as e:
        await ctx.error(f"Failed to get nodes status: {str(e)}")
        raise


@mcp.tool()
async def start_nodes(
    ctx: Context,
    nodes_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Start specified nodes.

    Args:
        nodes_data: Data specifying which nodes to start
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing operation status
    """
    await ctx.info("Tool called: start_nodes")
    await ctx.debug("Starting specified nodes")

    try:
        result = await start_nodes_api(nodes_data, domain)
        await ctx.info("Nodes started successfully")
        return result
    except Exception as e:
        await ctx.error(f"Failed to start nodes: {str(e)}")
        raise


@mcp.tool()
async def stop_nodes(
    ctx: Context,
    nodes_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Stop specified nodes.

    Args:
        nodes_data: Data specifying which nodes to stop
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing operation status
    """
    await ctx.info("Tool called: stop_nodes")
    await ctx.debug("Stopping specified nodes")

    try:
        result = await stop_nodes_api(nodes_data, domain)
        await ctx.info("Nodes stopped successfully")
        return result
    except Exception as e:
        await ctx.error(f"Failed to stop nodes: {str(e)}")
        raise
