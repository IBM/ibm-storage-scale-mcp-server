"""IBM Storage Scale Fileset operations."""

from typing import Optional, Any
from scale_mcp_server.utils.client import StorageScaleClient, StorageScaleAPIError


async def list_filesets_api(
    filesystem: str,
    domain: Optional[str] = None,
) -> Any:
    """List all filesets in a filesystem.

    Args:
        filesystem: Filesystem name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing filesets information

    Raises:
        StorageScaleAPIError: If the API request fails
    """
    headers = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.get(
                f"/scalemgmt/v3/filesystems/{filesystem}/filesets", headers=headers
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to list filesets for filesystem '{filesystem}': {str(e)}"
        ) from e


async def create_fileset_api(
    filesystem: str,
    fileset_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Create a new fileset in a filesystem.

    ⚠️ CRITICAL: The 'inodeSpace' parameter is IMMUTABLE after creation!
    - inodeSpace="new": Creates INDEPENDENT fileset (own inode space, can snapshot)
    - inodeSpace not "new": Creates DEPENDENT fileset (shared inode space, no independent snapshots)

    Args:
        filesystem: Filesystem name
        fileset_data: Fileset configuration data including:
            - filesetName (required): Name of the fileset
            - inodeSpace (CRITICAL): "new" for independent, omit for dependent
            - path, owner, permissions, comment (optional)
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing fileset creation status

    Raises:
        StorageScaleAPIError: If the API request fails
    """
    headers = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.post(
                f"/scalemgmt/v3/filesystems/{filesystem}/filesets",
                json=fileset_data,
                headers=headers,
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to create fileset in filesystem '{filesystem}': {str(e)}"
        ) from e


async def get_fileset_api(
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

    Raises:
        StorageScaleAPIError: If the API request fails
    """
    headers = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.get(
                f"/scalemgmt/v3/filesystems/{filesystem}/filesets/{fileset_name}",
                headers=headers,
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to get fileset '{fileset_name}' in filesystem '{filesystem}': {str(e)}"
        ) from e


async def delete_fileset_api(
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

    Raises:
        StorageScaleAPIError: If the API request fails
    """
    headers = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.delete(
                f"/scalemgmt/v3/filesystems/{filesystem}/filesets/{fileset_name}",
                headers=headers,
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to delete fileset '{fileset_name}' in filesystem '{filesystem}': {str(e)}"
        ) from e


async def update_fileset_api(
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

    Raises:
        StorageScaleAPIError: If the API request fails
    """
    headers = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.patch(
                f"/scalemgmt/v3/filesystems/{filesystem}/filesets/{fileset_name}",
                json=fileset_data,
                headers=headers,
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to update fileset '{fileset_name}' in filesystem '{filesystem}': {str(e)}"
        ) from e


async def get_fileset_usage_api(
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

    Raises:
        StorageScaleAPIError: If the API request fails
    """
    headers = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.get(
                f"/scalemgmt/v3/filesystems/{filesystem}/filesets/{fileset_name}/usage",
                headers=headers,
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to get usage for fileset '{fileset_name}' in filesystem '{filesystem}': {str(e)}"
        ) from e


async def link_fileset_api(
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

    Raises:
        StorageScaleAPIError: If the API request fails
    """
    headers = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.post(
                f"/scalemgmt/v3/filesystems/{filesystem}/filesets/{fileset_name}:link",
                json=link_data,
                headers=headers,
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to link fileset '{fileset_name}' in filesystem '{filesystem}': {str(e)}"
        ) from e


async def unlink_fileset_api(
    filesystem: str,
    fileset_name: str,
    unlink_data: Optional[dict] = None,
    domain: Optional[str] = None,
) -> Any:
    """Unlink a fileset from its junction path.

    Args:
        filesystem: Filesystem name
        fileset_name: Fileset name
        unlink_data: Unlink configuration data (e.g., {"force": true})
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing unlink status

    Raises:
        StorageScaleAPIError: If the API request fails
    """
    headers = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    # API requires a body, default to empty object if not provided
    body = unlink_data if unlink_data is not None else {}

    try:
        async with StorageScaleClient() as client:
            return await client.post(
                f"/scalemgmt/v3/filesystems/{filesystem}/filesets/{fileset_name}:unlink",
                json=body,
                headers=headers,
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to unlink fileset '{fileset_name}' in filesystem '{filesystem}': {str(e)}"
        ) from e


async def list_fileset_snapshots_api(
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

    Raises:
        StorageScaleAPIError: If the API request fails
    """
    headers = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.get(
                f"/scalemgmt/v3/filesystems/{filesystem}/filesets/{fileset}/snapshots",
                headers=headers,
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to list snapshots for fileset '{fileset}' in filesystem '{filesystem}': {str(e)}"
        ) from e


async def create_fileset_snapshot_api(
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

    Raises:
        StorageScaleAPIError: If the API request fails
    """
    headers = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.post(
                f"/scalemgmt/v3/filesystems/{filesystem}/filesets/{fileset}/snapshots",
                json=snapshot_data,
                headers=headers,
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to create snapshot for fileset '{fileset}' in filesystem '{filesystem}': {str(e)}"
        ) from e


async def get_fileset_snapshot_api(
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

    Raises:
        StorageScaleAPIError: If the API request fails
    """
    headers = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.get(
                f"/scalemgmt/v3/filesystems/{filesystem}/filesets/{fileset}/snapshots/{snapshot_name}",
                headers=headers,
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to get snapshot '{snapshot_name}' for fileset '{fileset}' in filesystem '{filesystem}': {str(e)}"
        ) from e


async def delete_fileset_snapshot_api(
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

    Raises:
        StorageScaleAPIError: If the API request fails
    """
    headers = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.delete(
                f"/scalemgmt/v3/filesystems/{filesystem}/filesets/{fileset}/snapshots/{snapshot_name}",
                headers=headers,
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to delete snapshot '{snapshot_name}' for fileset '{fileset}' in filesystem '{filesystem}': {str(e)}"
        ) from e


async def batch_create_fileset_snapshots_api(
    filesystem: str,
    snapshot_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Create snapshots for multiple filesets.

    Args:
        filesystem: Filesystem name
        snapshot_data: Batch snapshot creation data
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing creation status

    Raises:
        StorageScaleAPIError: If the API request fails
    """
    headers = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.post(
                f"/scalemgmt/v3/filesystems/{filesystem}/filesets/snapshots:batchCreate",
                json=snapshot_data,
                headers=headers,
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to batch create fileset snapshots in filesystem '{filesystem}': {str(e)}"
        ) from e


async def batch_delete_fileset_snapshots_api(
    filesystem: str,
    snapshot_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Delete snapshots for multiple filesets.

    Args:
        filesystem: Filesystem name
        snapshot_data: Batch snapshot deletion data
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing deletion status

    Raises:
        StorageScaleAPIError: If the API request fails
    """
    headers = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.post(
                f"/scalemgmt/v3/filesystems/{filesystem}/filesets/snapshots:batchDelete",
                json=snapshot_data,
                headers=headers,
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to batch delete fileset snapshots in filesystem '{filesystem}': {str(e)}"
        ) from e
