"""IBM Storage Scale Configuration Management MCP Server."""

from typing import Optional, Any
from fastmcp import FastMCP, Context
from scale_mcp_server.api.v3.config import (
    get_admin_config_api,
    update_admin_config_api,
)

# Create the config MCP server
mcp = FastMCP("config", instructions="Configuration management operations")


@mcp.tool()
async def get_admin_config(
    ctx: Context,
    domain: Optional[str] = None,
) -> Any:
    """Get admin configuration.

    Args:
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing admin configuration
    """
    await ctx.info("Tool called: get_admin_config")
    await ctx.debug("Retrieving admin configuration")

    try:
        result = await get_admin_config_api(domain=domain)
        await ctx.info("Successfully retrieved admin configuration")
        return result
    except Exception as e:
        await ctx.error(f"Failed to get admin config: {str(e)}")
        raise


@mcp.tool()
async def update_admin_config(
    ctx: Context,
    config_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Update admin configuration.

    Args:
        config_data: Configuration data
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing updated configuration
    """
    await ctx.info("Tool called: update_admin_config")
    await ctx.debug("Updating admin configuration")

    try:
        result = await update_admin_config_api(config_data=config_data, domain=domain)
        await ctx.info("Admin configuration updated successfully")
        return result
    except Exception as e:
        await ctx.error(f"Failed to update admin config: {str(e)}")
        raise
