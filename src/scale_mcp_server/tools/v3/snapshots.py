"""IBM Storage Scale Snapshot Management MCP Server."""

from typing import Optional, Any
from fastmcp import FastMCP, Context
from scale_mcp_server.api.v3.snapshots import (
    list_snapshots_api,
    create_snapshot_api,
    get_snapshot_api,
    delete_snapshot_api,
    get_snapdir_settings_api,
)
from scale_mcp_server.api.v3.filesets import (
    list_fileset_snapshots_api,
    create_fileset_snapshot_api,
    get_fileset_snapshot_api,
    delete_fileset_snapshot_api,
)

# Create the snapshots MCP server
mcp = FastMCP("snapshots", instructions="Snapshot management operations")


@mcp.tool()
async def list_filesystem_snapshots(
    ctx: Context,
    filesystem: str,
    domain: Optional[str] = None,
) -> Any:
    """List all snapshots for a filesystem.

    Args:
        filesystem: Filesystem name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing snapshots information
    """
    await ctx.info(
        f"Tool called: list_filesystem_snapshots with filesystem={filesystem}"
    )
    await ctx.debug(f"Listing all snapshots for filesystem: {filesystem}")

    try:
        result = await list_snapshots_api(filesystem=filesystem, domain=domain)
        await ctx.info(f"Successfully retrieved snapshots for {filesystem}")
        return result
    except Exception as e:
        await ctx.error(f"Failed to list snapshots for {filesystem}: {str(e)}")
        raise


@mcp.tool()
async def create_filesystem_snapshot(
    ctx: Context,
    filesystem: str,
    snapshot_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Create a new filesystem snapshot.

    Args:
        filesystem: Filesystem name
        snapshot_data: Snapshot configuration data
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing snapshot information
    """
    await ctx.info(
        f"Tool called: create_filesystem_snapshot with filesystem={filesystem}"
    )
    await ctx.debug(f"Creating new snapshot for filesystem: {filesystem}")

    try:
        result = await create_snapshot_api(
            filesystem=filesystem, snapshot_data=snapshot_data, domain=domain
        )
        await ctx.info(f"Snapshot created successfully for {filesystem}")
        return result
    except Exception as e:
        await ctx.error(f"Failed to create snapshot for {filesystem}: {str(e)}")
        raise


@mcp.tool()
async def get_filesystem_snapshot(
    ctx: Context,
    filesystem: str,
    snapshot_name: str,
    domain: Optional[str] = None,
) -> Any:
    """Get information about a specific filesystem snapshot.

    Args:
        filesystem: Filesystem name
        snapshot_name: Snapshot name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing snapshot information
    """
    await ctx.info(
        f"Tool called: get_filesystem_snapshot with filesystem={filesystem}, snapshot_name={snapshot_name}"
    )
    await ctx.debug(f"Retrieving snapshot {snapshot_name} from filesystem {filesystem}")

    try:
        result = await get_snapshot_api(
            filesystem=filesystem, snapshot_name=snapshot_name, domain=domain
        )
        await ctx.info(f"Successfully retrieved snapshot {snapshot_name}")
        return result
    except Exception as e:
        await ctx.error(f"Failed to get snapshot {snapshot_name}: {str(e)}")
        raise


@mcp.tool()
async def delete_filesystem_snapshot(
    ctx: Context,
    filesystem: str,
    snapshot_name: str,
    domain: Optional[str] = None,
) -> Any:
    """Delete a filesystem snapshot.

    Args:
        filesystem: Filesystem name
        snapshot_name: Snapshot name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing deletion status
    """
    await ctx.info(
        f"Tool called: delete_filesystem_snapshot with filesystem={filesystem}, snapshot_name={snapshot_name}"
    )
    await ctx.debug(f"Deleting snapshot {snapshot_name} from filesystem {filesystem}")

    try:
        result = await delete_snapshot_api(
            filesystem=filesystem, snapshot_name=snapshot_name, domain=domain
        )
        await ctx.info(f"Snapshot {snapshot_name} deleted successfully")
        return result
    except Exception as e:
        await ctx.error(f"Failed to delete snapshot {snapshot_name}: {str(e)}")
        raise


@mcp.tool()
async def list_fileset_snapshots(
    ctx: Context,
    filesystem: str,
    fileset: str,
    domain: Optional[str] = None,
) -> Any:
    """List snapshots for a fileset.

    Args:
        filesystem: Filesystem name
        fileset: Fileset name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing fileset snapshots information
    """
    await ctx.info(
        f"Tool called: list_fileset_snapshots with filesystem={filesystem}, fileset={fileset}"
    )
    await ctx.debug(f"Listing snapshots for fileset {fileset}")

    try:
        result = await list_fileset_snapshots_api(
            filesystem=filesystem, fileset=fileset, domain=domain
        )
        await ctx.info(f"Successfully retrieved snapshots for fileset {fileset}")
        return result
    except Exception as e:
        await ctx.error(f"Failed to list snapshots for fileset {fileset}: {str(e)}")
        raise


@mcp.tool()
async def create_fileset_snapshot(
    ctx: Context,
    filesystem: str,
    fileset: str,
    snapshot_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Create a snapshot for a fileset.

    Args:
        filesystem: Filesystem name
        fileset: Fileset name
        snapshot_data: Snapshot configuration data
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing snapshot creation status
    """
    await ctx.info(
        f"Tool called: create_fileset_snapshot with filesystem={filesystem}, fileset={fileset}"
    )
    await ctx.debug(f"Creating snapshot for fileset {fileset}")

    try:
        result = await create_fileset_snapshot_api(
            filesystem=filesystem,
            fileset=fileset,
            snapshot_data=snapshot_data,
            domain=domain,
        )
        await ctx.info(f"Successfully created snapshot for fileset {fileset}")
        return result
    except Exception as e:
        await ctx.error(f"Failed to create snapshot for fileset {fileset}: {str(e)}")
        raise


@mcp.tool()
async def get_fileset_snapshot(
    ctx: Context,
    filesystem: str,
    fileset: str,
    snapshot_name: str,
    domain: Optional[str] = None,
) -> Any:
    """Get information about a specific fileset snapshot.

    Args:
        filesystem: Filesystem name
        fileset: Fileset name
        snapshot_name: Snapshot name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing snapshot information
    """
    await ctx.info(
        f"Tool called: get_fileset_snapshot with filesystem={filesystem}, fileset={fileset}, snapshot_name={snapshot_name}"
    )
    await ctx.debug(f"Retrieving snapshot {snapshot_name} for fileset {fileset}")

    try:
        result = await get_fileset_snapshot_api(
            filesystem=filesystem,
            fileset=fileset,
            snapshot_name=snapshot_name,
            domain=domain,
        )
        await ctx.info(
            f"Successfully retrieved snapshot {snapshot_name} for fileset {fileset}"
        )
        return result
    except Exception as e:
        await ctx.error(
            f"Failed to get snapshot {snapshot_name} for fileset {fileset}: {str(e)}"
        )
        raise


@mcp.tool()
async def delete_fileset_snapshot(
    ctx: Context,
    filesystem: str,
    fileset: str,
    snapshot_name: str,
    domain: Optional[str] = None,
) -> Any:
    """Delete a fileset snapshot.

    Args:
        filesystem: Filesystem name
        fileset: Fileset name
        snapshot_name: Snapshot name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing deletion status
    """
    await ctx.info(
        f"Tool called: delete_fileset_snapshot with filesystem={filesystem}, fileset={fileset}, snapshot_name={snapshot_name}"
    )
    await ctx.debug(f"Deleting snapshot {snapshot_name} for fileset {fileset}")

    try:
        result = await delete_fileset_snapshot_api(
            filesystem=filesystem,
            fileset=fileset,
            snapshot_name=snapshot_name,
            domain=domain,
        )
        await ctx.info(
            f"Successfully deleted snapshot {snapshot_name} for fileset {fileset}"
        )
        return result
    except Exception as e:
        await ctx.error(
            f"Failed to delete snapshot {snapshot_name} for fileset {fileset}: {str(e)}"
        )
        raise


@mcp.tool()
async def get_snapdir_settings(
    ctx: Context,
    filesystem: str,
    domain: Optional[str] = None,
) -> Any:
    """Get snapdir settings for a filesystem.

    Args:
        filesystem: Filesystem name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing snapdir settings
    """
    await ctx.info(f"Tool called: get_snapdir_settings with filesystem={filesystem}")
    await ctx.debug(f"Retrieving snapdir settings for filesystem: {filesystem}")

    try:
        result = await get_snapdir_settings_api(filesystem=filesystem, domain=domain)
        await ctx.info(f"Successfully retrieved snapdir settings for {filesystem}")
        return result
    except Exception as e:
        await ctx.error(f"Failed to get snapdir settings for {filesystem}: {str(e)}")
        raise
