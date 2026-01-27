"""IBM Storage Scale Node Health Management MCP Server (v2 API)."""

from typing import Optional, Any
from fastmcp import FastMCP, Context
from scale_mcp_server.api.v2.nodes import (
    get_node_health_states_api,
    get_node_health_events_api,
)

# Create the nodes health MCP server
mcp = FastMCP(
    "nodes_health_v2", instructions="Node health monitoring operations (v2 API)"
)


@mcp.tool()
async def get_node_health_states(
    ctx: Context,
    name: str,
    fields: Optional[str] = None,
    filter: Optional[str] = None,
) -> Any:
    """Get System Health states for a node or nodeclass.

    Returns a list of currently active System Health states for the given node or nodeclass.

    Args:
        name: Nodeclass, node name or ':all:'
        fields: Comma separated list of fields to be included in response. ':all:' selects all available fields
        filter: Filter objects by expression, e.g. 'status=HEALTHY,entityType=FILESET'

    Returns:
        Dictionary containing system health states information
    """
    await ctx.info(f"Tool called: get_node_health_states for node: {name}")
    await ctx.debug(f"Retrieving health states for node: {name}")

    try:
        result = await get_node_health_states_api(
            name=name, fields=fields, filter=filter
        )
        await ctx.info(f"Successfully retrieved health states for node: {name}")
        return result
    except Exception as e:
        await ctx.error(f"Failed to get health states for node {name}: {str(e)}")
        raise


@mcp.tool()
async def get_node_health_events(
    ctx: Context,
    name: str,
    fields: Optional[str] = None,
    filter: Optional[str] = None,
) -> Any:
    """Get System Health events for a node or nodeclass.

    Returns a list of currently active System Health events for the given node or nodeclass.

    Args:
        name: Nodeclass, node name or ':all:'
        fields: Comma separated list of fields to be included in response. ':all:' selects all available fields
        filter: Filter objects by expression, e.g. 'status=HEALTHY,entityType=FILESET'

    Returns:
        Dictionary containing system health events information
    """
    await ctx.info(f"Tool called: get_node_health_events for node: {name}")
    await ctx.debug(f"Retrieving health events for node: {name}")

    try:
        result = await get_node_health_events_api(
            name=name, fields=fields, filter=filter
        )
        await ctx.info(f"Successfully retrieved health events for node: {name}")
        return result
    except Exception as e:
        await ctx.error(f"Failed to get health events for node {name}: {str(e)}")
        raise
