"""IBM Storage Scale NSD Management MCP Server."""

from typing import Optional, Any
from fastmcp import FastMCP, Context
from scale_mcp_server.api.v3.nsds import (
    list_nsds_api,
    get_nsd_api,
)

# Create the nsds MCP server
mcp = FastMCP("nsds", instructions="NSD (Network Shared Disk) management operations")


@mcp.tool()
async def list_nsds(
    ctx: Context,
    domain: Optional[str] = None,
) -> Any:
    """List all NSDs (Network Shared Disks).

    Args:
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing NSDs information
    """
    await ctx.info("Tool called: list_nsds")
    await ctx.debug("Listing all NSDs (Network Shared Disks)")

    try:
        result = await list_nsds_api(domain=domain)
        await ctx.info("Successfully retrieved NSDs list")
        return result
    except Exception as e:
        await ctx.error(f"Failed to list NSDs: {str(e)}")
        raise


@mcp.tool()
async def get_nsd(
    ctx: Context,
    nsd_name: str,
    domain: Optional[str] = None,
) -> Any:
    """Get information about a specific NSD.

    Args:
        nsd_name: NSD name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing NSD information
    """
    await ctx.info(f"Tool called: get_nsd with nsd_name={nsd_name}")
    await ctx.debug(f"Retrieving information for NSD: {nsd_name}")

    try:
        result = await get_nsd_api(nsd_name=nsd_name, domain=domain)
        await ctx.info(f"Successfully retrieved NSD: {nsd_name}")
        return result
    except Exception as e:
        await ctx.error(f"Failed to get NSD {nsd_name}: {str(e)}")
        raise
