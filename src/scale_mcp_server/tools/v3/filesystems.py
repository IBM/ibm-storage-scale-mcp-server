"""IBM Storage Scale Filesystem Management MCP Server."""

from typing import Optional, Any
from fastmcp import FastMCP, Context
from scale_mcp_server.api.v3.filesystems import (
    list_filesystems_api,
    get_filesystem_api,
    delete_filesystem_api,
    mount_filesystem_api,
    unmount_filesystem_api,
    mount_all_filesystems_api,
    unmount_all_filesystems_api,
)

# Create the filesystems MCP server
mcp = FastMCP("filesystems", instructions="Filesystem management operations")


@mcp.tool()
async def list_filesystems(
    ctx: Context,
    domain: Optional[str] = None,
) -> Any:
    """List all filesystems.

    Args:
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing filesystems information
    """
    await ctx.info("Tool called: list_filesystems")
    await ctx.debug("Listing all filesystems")

    try:
        result = await list_filesystems_api(domain=domain)
        await ctx.info("Successfully retrieved filesystems list")
        return result
    except Exception as e:
        await ctx.error(f"Failed to list filesystems: {str(e)}")
        raise


@mcp.tool()
async def get_filesystem(
    ctx: Context,
    filesystem: str,
    domain: Optional[str] = None,
) -> Any:
    """Get information about a specific filesystem.

    Args:
        filesystem: Filesystem name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing filesystem information
    """
    await ctx.info(f"Tool called: get_filesystem with filesystem={filesystem}")
    await ctx.debug(f"Retrieving information for filesystem: {filesystem}")

    headers = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        result = await get_filesystem_api(filesystem=filesystem, domain=domain)
        await ctx.info(f"Successfully retrieved filesystem: {filesystem}")
        return result
    except Exception as e:
        await ctx.error(f"Failed to get filesystem {filesystem}: {str(e)}")
        raise


@mcp.tool()
async def delete_filesystem(
    ctx: Context,
    name: str,
    domain: Optional[str] = None,
) -> Any:
    """Delete a filesystem.

    Args:
        name: Filesystem name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing deletion status
    """
    await ctx.info(f"Tool called: delete_filesystem with name={name}")
    await ctx.debug(f"Deleting filesystem: {name}")

    headers = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        result = await delete_filesystem_api(name=name, domain=domain)
        await ctx.info(f"Filesystem {name} deleted successfully")
        return result
    except Exception as e:
        await ctx.error(f"Failed to delete filesystem {name}: {str(e)}")
        raise


@mcp.tool()
async def mount_filesystem(
    ctx: Context,
    filesystem: str,
    nodes: Optional[str] = None,
    domain: Optional[str] = None,
) -> Any:
    """Mount a filesystem.

    Args:
        filesystem: Filesystem name
        mount_data: Mount configuration data
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing mount status
    """
    await ctx.info(f"Tool called: mount_filesystem with filesystem={filesystem}")
    await ctx.debug(f"Mounting filesystem: {filesystem}")

    headers = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        result = await mount_filesystem_api(name=filesystem, nodes=nodes, domain=domain)
        await ctx.info(f"Filesystem {filesystem} mounted successfully")
        return result
    except Exception as e:
        await ctx.error(f"Failed to mount filesystem {filesystem}: {str(e)}")
        raise


@mcp.tool()
async def unmount_filesystem(
    ctx: Context,
    filesystem: str,
    nodes: Optional[str] = None,
    domain: Optional[str] = None,
) -> Any:
    """Unmount a filesystem.

    Args:
        filesystem: Filesystem name
        unmount_data: Unmount configuration data
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing unmount status
    """
    await ctx.info(f"Tool called: unmount_filesystem with filesystem={filesystem}")
    await ctx.debug(f"Unmounting filesystem: {filesystem}")

    headers = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        result = await unmount_filesystem_api(
            name=filesystem, nodes=nodes, domain=domain
        )
        await ctx.info(f"Filesystem {filesystem} unmounted successfully")
        return result
    except Exception as e:
        await ctx.error(f"Failed to unmount filesystem {filesystem}: {str(e)}")
        raise


@mcp.tool()
async def mount_all_filesystems(
    ctx: Context,
    mount_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Mount all filesystems.

    Args:
        mount_data: Mount configuration data
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing mount status
    """
    await ctx.info("Tool called: mount_all_filesystems")
    await ctx.debug("Mounting all filesystems")

    headers = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        result = await mount_all_filesystems_api(domain=domain)
        await ctx.info("All filesystems mounted successfully")
        return result
    except Exception as e:
        await ctx.error(f"Failed to mount all filesystems: {str(e)}")
        raise


@mcp.tool()
async def unmount_all_filesystems(
    ctx: Context,
    unmount_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Unmount all filesystems.

    Args:
        unmount_data: Unmount configuration data
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing unmount status
    """
    await ctx.info("Tool called: unmount_all_filesystems")
    await ctx.debug("Unmounting all filesystems")

    headers = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        result = await unmount_all_filesystems_api(domain=domain)
        await ctx.info("All filesystems unmounted successfully")
        return result
    except Exception as e:
        await ctx.error(f"Failed to unmount all filesystems: {str(e)}")
        raise
