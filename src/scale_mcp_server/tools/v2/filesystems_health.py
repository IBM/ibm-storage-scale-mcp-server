"""IBM Storage Scale Filesystem Health Management MCP Server (v2 API)."""

from typing import Any
from fastmcp import FastMCP, Context
from scale_mcp_server.api.v2.filesystems import (
    get_filesystem_health_states_api,
    get_filesystem_health_events_api,
)

# Create the filesystems health MCP server
mcp = FastMCP(
    "filesystems_health_v2",
    instructions="Filesystem health monitoring operations (v2 API)",
)


@mcp.tool()
async def get_filesystem_health_states(
    ctx: Context,
    filesystem: str,
) -> Any:
    """Get Cluster Related health State for a filesystem.

    Returns the health state for the specified filesystem.

    Args:
        filesystem: Filesystem name

    Returns:
        Dictionary containing filesystem health state information
    """
    await ctx.info(
        f"Tool called: get_filesystem_health_states for filesystem: {filesystem}"
    )
    await ctx.debug(f"Retrieving health states for filesystem: {filesystem}")

    try:
        result = await get_filesystem_health_states_api(filesystem=filesystem)
        await ctx.info(
            f"Successfully retrieved health states for filesystem: {filesystem}"
        )
        return result
    except Exception as e:
        await ctx.error(
            f"Failed to get health states for filesystem {filesystem}: {str(e)}"
        )
        raise


@mcp.tool()
async def get_filesystem_health_events(
    ctx: Context,
    filesystem_name: str,
) -> Any:
    """Get Cluster Related System Health events for a filesystem.

    Returns a list of currently active Cluster related System Health events for the specified filesystem.

    Args:
        filesystem_name: Filesystem name

    Returns:
        Dictionary containing filesystem health events information
    """
    await ctx.info(
        f"Tool called: get_filesystem_health_events for filesystem: {filesystem_name}"
    )
    await ctx.debug(f"Retrieving health events for filesystem: {filesystem_name}")

    try:
        result = await get_filesystem_health_events_api(filesystem_name=filesystem_name)
        await ctx.info(
            f"Successfully retrieved health events for filesystem: {filesystem_name}"
        )
        return result
    except Exception as e:
        await ctx.error(
            f"Failed to get health events for filesystem {filesystem_name}: {str(e)}"
        )
        raise
