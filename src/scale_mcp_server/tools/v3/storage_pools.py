"""IBM Storage Scale Storage Pool Management MCP Server."""

from typing import Optional, Any
from fastmcp import FastMCP, Context
from scale_mcp_server.api.v3.storage_pools import (
    list_storage_pools_api,
    get_storage_pool_api,
)

# Create the storage_pools MCP server
mcp = FastMCP("storage_pools", instructions="Storage pool management operations")


@mcp.tool()
async def list_storage_pools(
    ctx: Context,
    filesystem: str,
    domain: Optional[str] = None,
) -> Any:
    """List storage pools for a filesystem.

    Args:
        filesystem: Filesystem name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing storage pools information
    """
    await ctx.info(f"Tool called: list_storage_pools with filesystem={filesystem}")
    await ctx.debug(f"Listing storage pools for filesystem: {filesystem}")

    try:
        result = await list_storage_pools_api(filesystem=filesystem, domain=domain)
        await ctx.info(f"Successfully retrieved storage pools for {filesystem}")
        return result
    except Exception as e:
        await ctx.error(f"Failed to list storage pools for {filesystem}: {str(e)}")
        raise


@mcp.tool()
async def get_storage_pool(
    ctx: Context,
    filesystem: str,
    pool_name: str,
    domain: Optional[str] = None,
) -> Any:
    """Get information about a specific storage pool.

    Args:
        filesystem: Filesystem name
        pool_name: Storage pool name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing storage pool information
    """
    await ctx.info(
        f"Tool called: get_storage_pool with filesystem={filesystem}, pool_name={pool_name}"
    )
    await ctx.debug(f"Retrieving storage pool {pool_name} from filesystem {filesystem}")

    try:
        result = await get_storage_pool_api(
            filesystem=filesystem, pool_name=pool_name, domain=domain
        )
        await ctx.info(f"Successfully retrieved storage pool {pool_name}")
        return result
    except Exception as e:
        await ctx.error(f"Failed to get storage pool {pool_name}: {str(e)}")
        raise
