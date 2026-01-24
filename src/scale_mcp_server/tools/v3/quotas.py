"""IBM Storage Scale Quota Management MCP Server."""

from typing import Optional, Any
from fastmcp import FastMCP, Context
from scale_mcp_server.api.v3.quotas import (
    list_quotas_api,
    set_quota_api,
)

# Create the quotas MCP server
mcp = FastMCP("quotas", instructions="Quota management operations")


@mcp.tool()
async def list_quotas(
    ctx: Context,
    filesystem: str,
    domain: Optional[str] = None,
) -> Any:
    """List all quotas for a filesystem.

    Args:
        filesystem: Filesystem name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing quotas information
    """
    await ctx.info(f"Tool called: list_quotas with filesystem={filesystem}")
    await ctx.debug(f"Listing all quotas for filesystem: {filesystem}")

    try:
        result = await list_quotas_api(filesystem=filesystem, domain=domain)
        await ctx.info(f"Successfully retrieved quotas for {filesystem}")
        return result
    except Exception as e:
        await ctx.error(f"Failed to list quotas for {filesystem}: {str(e)}")
        raise


@mcp.tool()
async def set_quota(
    ctx: Context,
    filesystem: str,
    quota_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Set or update a quota.

    Args:
        filesystem: Filesystem name
        quota_data: Quota configuration data
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing quota information
    """
    await ctx.info(f"Tool called: set_quota with filesystem={filesystem}")
    await ctx.debug(f"Setting/updating quota for filesystem: {filesystem}")

    try:
        result = await set_quota_api(
            filesystem=filesystem, quota_data=quota_data, domain=domain
        )
        await ctx.info(f"Quota set successfully for {filesystem}")
        return result
    except Exception as e:
        await ctx.error(f"Failed to set quota for {filesystem}: {str(e)}")
        raise
