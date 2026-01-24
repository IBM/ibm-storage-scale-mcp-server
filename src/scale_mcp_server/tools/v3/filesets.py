"""IBM Storage Scale Fileset Management MCP Server."""

from typing import Optional, Any
from fastmcp import FastMCP, Context
from scale_mcp_server.api.v3.filesets import (
    list_filesets_api,
    create_fileset_api,
    get_fileset_api,
    delete_fileset_api,
    update_fileset_api,
    get_fileset_usage_api,
    link_fileset_api,
    unlink_fileset_api,
)

# Create the filesets MCP server
mcp = FastMCP("filesets", instructions="Fileset management operations")


@mcp.tool()
async def list_filesets(
    ctx: Context,
    filesystem: str,
    domain: Optional[str] = None,
) -> Any:
    """List all filesets in a filesystem.

    Args:
        filesystem: Filesystem name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing filesets information
    """
    await ctx.info(f"Tool called: list_filesets with filesystem={filesystem}")
    await ctx.debug(f"Listing all filesets for filesystem: {filesystem}")

    try:
        result = await list_filesets_api(filesystem=filesystem, domain=domain)
        await ctx.info(f"Successfully retrieved filesets for {filesystem}")
        return result
    except Exception as e:
        await ctx.error(f"Failed to list filesets for {filesystem}: {str(e)}")
        raise


@mcp.tool()
async def create_independent_fileset(
    ctx: Context,
    filesystem: str,
    fileset_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Create an INDEPENDENT fileset with its own inode space.

    INDEPENDENT FILESET CHARACTERISTICS:
    - Has its own inode space (inode_space_designation="new" - automatically set by this tool)
    - Can have snapshots
    - Can have quotas
    - Higher overhead due to separate inode allocation
    - This choice is PERMANENT and cannot be changed after creation!

    Use this when you need:
    - Independent snapshot capability
    - Isolated quota management

    Args:
        filesystem: Filesystem name
        fileset_data: Fileset configuration (filesetName, path, owner, permissions, comment, etc.)
                     Note: inode_space_designation will be automatically set to "new" by this tool
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing fileset creation status

    Example:
        create_independent_fileset(
            filesystem="gpfs1",
            fileset_data={
                "filesetName": "project_data",
                "path": "/gpfs/gpfs1/projects/data",
                "comment": "Independent fileset for project data"
            }
        )
    """
    await ctx.info(
        f"Tool called: create_independent_fileset with filesystem={filesystem}"
    )
    await ctx.warning(
        "Creating INDEPENDENT fileset with own inode space. "
        "This is PERMANENT and cannot be changed!"
    )

    # Set inode_space_designation to "new" for independent fileset
    fileset_data["inode_space_designation"] = "new"

    await ctx.debug(f"Fileset data: {fileset_data}")

    try:
        result = await create_fileset_api(
            filesystem=filesystem, fileset_data=fileset_data, domain=domain
        )
        await ctx.info(f"Successfully created INDEPENDENT fileset in {filesystem}")
        return result
    except Exception as e:
        await ctx.error(
            f"Failed to create independent fileset in {filesystem}: {str(e)}"
        )
        raise


@mcp.tool()
async def create_dependent_fileset(
    ctx: Context,
    filesystem: str,
    fileset_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Create a DEPENDENT fileset that shares the parent's inode space.

    DEPENDENT FILESET CHARACTERISTICS:
    - Shares parent filesystem's inode space (inode_space_designation NOT set to "new")
    - CANNOT have independent snapshots
    - Shares quota space with parent
    - Lower overhead, more efficient
    - This choice is PERMANENT and cannot be changed after creation!

    Use this when you need:
    - Lower overhead and better performance
    - Shared resource management
    - Simple directory organization

    Args:
        filesystem: Filesystem name
        fileset_data: Fileset configuration (filesetName, path, owner, permissions, comment, etc.)
                     Note: inode_space_designation will NOT be set (or will be removed if present)
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing fileset creation status

    Example:
        create_dependent_fileset(
            filesystem="gpfs1",
            fileset_data={
                "filesetName": "temp_data",
                "path": "/gpfs/gpfs1/temp",
                "comment": "Dependent fileset for temporary data"
            }
        )
    """
    await ctx.info(
        f"Tool called: create_dependent_fileset with filesystem={filesystem}"
    )
    await ctx.warning(
        "Creating DEPENDENT fileset sharing parent's inode space. "
        "This is PERMANENT and cannot be changed!"
    )

    # Ensure inode_space_designation is NOT set for dependent fileset
    fileset_data.pop("inode_space_designation", None)

    await ctx.debug(f"Fileset data: {fileset_data}")

    try:
        result = await create_fileset_api(
            filesystem=filesystem, fileset_data=fileset_data, domain=domain
        )
        await ctx.info(f"✓ Successfully created DEPENDENT fileset in {filesystem}")
        return result
    except Exception as e:
        await ctx.error(f"Failed to create dependent fileset in {filesystem}: {str(e)}")
        raise


@mcp.tool()
async def get_fileset(
    ctx: Context,
    filesystem: str,
    fileset_name: str,
    domain: Optional[str] = None,
) -> Any:
    """Get information about a specific fileset.

    Args:
        filesystem: Filesystem name
        fileset_name: Fileset name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing fileset information
    """
    await ctx.info(
        f"Tool called: get_fileset with filesystem={filesystem}, fileset_name={fileset_name}"
    )
    await ctx.debug(f"Retrieving fileset {fileset_name} from filesystem {filesystem}")

    try:
        result = await get_fileset_api(
            filesystem=filesystem, fileset_name=fileset_name, domain=domain
        )
        await ctx.info(f"Successfully retrieved fileset {fileset_name}")
        return result
    except Exception as e:
        await ctx.error(f"Failed to get fileset {fileset_name}: {str(e)}")
        raise


@mcp.tool()
async def delete_fileset(
    ctx: Context,
    filesystem: str,
    fileset_name: str,
    domain: Optional[str] = None,
) -> Any:
    """Delete a fileset from a filesystem.

    Args:
        filesystem: Filesystem name
        fileset_name: Fileset name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing deletion status
    """
    await ctx.info(
        f"Tool called: delete_fileset with filesystem={filesystem}, fileset_name={fileset_name}"
    )
    await ctx.debug(f"Deleting fileset {fileset_name} from filesystem {filesystem}")

    try:
        result = await delete_fileset_api(
            filesystem=filesystem, fileset_name=fileset_name, domain=domain
        )
        await ctx.info(f"Successfully deleted fileset {fileset_name}")
        return result
    except Exception as e:
        await ctx.error(f"Failed to delete fileset {fileset_name}: {str(e)}")
        raise


@mcp.tool()
async def update_fileset(
    ctx: Context,
    filesystem: str,
    fileset_name: str,
    fileset_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Update a fileset's configuration.

    Args:
        filesystem: Filesystem name
        fileset_name: Fileset name
        fileset_data: Fileset update data
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing update status
    """
    await ctx.info(
        f"Tool called: update_fileset with filesystem={filesystem}, fileset_name={fileset_name}"
    )
    await ctx.debug(f"Updating fileset {fileset_name} in filesystem {filesystem}")

    try:
        result = await update_fileset_api(
            filesystem=filesystem,
            fileset_name=fileset_name,
            fileset_data=fileset_data,
            domain=domain,
        )
        await ctx.info(f"Successfully updated fileset {fileset_name}")
        return result
    except Exception as e:
        await ctx.error(f"Failed to update fileset {fileset_name}: {str(e)}")
        raise


@mcp.tool()
async def get_fileset_usage(
    ctx: Context,
    filesystem: str,
    fileset_name: str,
    domain: Optional[str] = None,
) -> Any:
    """Get usage information for a fileset.

    Args:
        filesystem: Filesystem name
        fileset_name: Fileset name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing fileset usage information
    """
    await ctx.info(
        f"Tool called: get_fileset_usage with filesystem={filesystem}, fileset_name={fileset_name}"
    )
    await ctx.debug(f"Retrieving usage for fileset {fileset_name}")

    try:
        result = await get_fileset_usage_api(
            filesystem=filesystem, fileset_name=fileset_name, domain=domain
        )
        await ctx.info(f"Successfully retrieved usage for fileset {fileset_name}")
        return result
    except Exception as e:
        await ctx.error(f"Failed to get fileset usage for {fileset_name}: {str(e)}")
        raise


@mcp.tool()
async def link_fileset(
    ctx: Context,
    filesystem: str,
    fileset_name: str,
    link_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Link a fileset to a junction path.

    Args:
        filesystem: Filesystem name
        fileset_name: Fileset name
        link_data: Link configuration data
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing link status
    """
    await ctx.info(
        f"Tool called: link_fileset with filesystem={filesystem}, fileset_name={fileset_name}"
    )
    await ctx.debug(f"Linking fileset {fileset_name} to junction path")

    try:
        result = await link_fileset_api(
            filesystem=filesystem,
            fileset_name=fileset_name,
            link_data=link_data,
            domain=domain,
        )
        await ctx.info(f"Fileset {fileset_name} linked successfully")
        return result
    except Exception as e:
        await ctx.error(f"Failed to link fileset {fileset_name}: {str(e)}")
        raise


@mcp.tool()
async def unlink_fileset(
    ctx: Context,
    filesystem: str,
    fileset_name: str,
    unlink_data: Optional[dict] = None,
    domain: Optional[str] = None,
) -> Any:
    """Unlink a fileset from its junction path.

    Args:
        filesystem: Filesystem name
        fileset_name: Fileset name
        unlink_data: Unlink configuration data
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing unlink status
    """
    await ctx.info(
        f"Tool called: unlink_fileset with filesystem={filesystem}, fileset_name={fileset_name}"
    )
    await ctx.debug(f"Unlinking fileset {fileset_name} from junction path")

    try:
        result = await unlink_fileset_api(
            filesystem=filesystem,
            fileset_name=fileset_name,
            unlink_data=unlink_data,
            domain=domain,
        )
        await ctx.info(f"Fileset {fileset_name} unlinked successfully")
        return result
    except Exception as e:
        await ctx.error(f"Failed to unlink fileset {fileset_name}: {str(e)}")
        raise
