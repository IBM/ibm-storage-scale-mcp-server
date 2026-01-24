"""IBM Storage Scale Policy Management MCP Server."""

from typing import Optional, Any
from fastmcp import FastMCP, Context
from scale_mcp_server.api.v3.policies import (
    get_policy_api,
    update_policy_api,
)

# Create the policies MCP server
mcp = FastMCP("policies", instructions="Policy management operations")


@mcp.tool()
async def get_policy(
    ctx: Context,
    filesystem: str,
    domain: Optional[str] = None,
) -> Any:
    """Get policy for a filesystem.

    Args:
        filesystem: Filesystem name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing policy information
    """
    await ctx.info(f"Tool called: get_policy with filesystem={filesystem}")
    await ctx.debug(f"Retrieving policy for filesystem: {filesystem}")

    try:
        result = await get_policy_api(filesystem=filesystem, domain=domain)
        await ctx.info(f"Successfully retrieved policy for {filesystem}")
        return result
    except Exception as e:
        await ctx.error(f"Failed to get policy for {filesystem}: {str(e)}")
        raise


@mcp.tool()
async def update_policy(
    ctx: Context,
    filesystem: str,
    policy_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Update policy for a filesystem.

    Args:
        filesystem: Filesystem name
        policy_data: Policy configuration data
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing updated policy information
    """
    await ctx.info(f"Tool called: update_policy with filesystem={filesystem}")
    await ctx.debug(f"Updating policy for filesystem: {filesystem}")

    try:
        result = await update_policy_api(
            filesystem=filesystem, policy_data=policy_data, domain=domain
        )
        await ctx.info(f"Policy for {filesystem} updated successfully")
        return result
    except Exception as e:
        await ctx.error(f"Failed to update policy for {filesystem}: {str(e)}")
        raise
