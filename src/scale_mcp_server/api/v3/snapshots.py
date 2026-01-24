"""IBM Storage Scale Snapshot operations."""

from typing import Optional, Any
from scale_mcp_server.utils.client import StorageScaleClient, StorageScaleAPIError


async def list_snapshots_api(
    filesystem: str,
    domain: Optional[str] = None,
) -> Any:
    """List all snapshots for a filesystem.

    Args:
        filesystem: Filesystem name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing snapshots information

    Raises:
        StorageScaleAPIError: If the API request fails
    """
    headers = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.get(
                f"/scalemgmt/v3/filesystems/{filesystem}/snapshots", headers=headers
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to list snapshots for filesystem '{filesystem}': {str(e)}"
        ) from e


async def create_snapshot_api(
    filesystem: str,
    snapshot_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Create a new snapshot.

    Args:
        filesystem: Filesystem name
        snapshot_data: Snapshot configuration data
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
            return await client.post(
                f"/scalemgmt/v3/filesystems/{filesystem}/snapshots",
                json=snapshot_data,
                headers=headers,
            )
    except StorageScaleAPIError as e:
        snapshot_name = snapshot_data.get("snapshotName", "unknown")
        raise StorageScaleAPIError(
            f"Failed to create snapshot '{snapshot_name}' for filesystem '{filesystem}': {str(e)}"
        ) from e


async def get_snapshot_api(
    filesystem: str,
    snapshot_name: str,
    domain: Optional[str] = None,
) -> Any:
    """Get information about a specific snapshot.

    Args:
        filesystem: Filesystem name
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
                f"/scalemgmt/v3/filesystems/{filesystem}/snapshots/{snapshot_name}",
                headers=headers,
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to get snapshot '{snapshot_name}' for filesystem '{filesystem}': {str(e)}"
        ) from e


async def delete_snapshot_api(
    filesystem: str,
    snapshot_name: str,
    domain: Optional[str] = None,
) -> Any:
    """Delete a snapshot.

    Args:
        filesystem: Filesystem name
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
                f"/scalemgmt/v3/filesystems/{filesystem}/snapshots/{snapshot_name}",
                headers=headers,
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to delete snapshot '{snapshot_name}' for filesystem '{filesystem}': {str(e)}"
        ) from e


async def batch_delete_snapshots_api(
    filesystem: str,
    snapshot_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Delete multiple snapshots.

    Args:
        filesystem: Filesystem name
        snapshot_data: Batch deletion data
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
                f"/scalemgmt/v3/filesystems/{filesystem}/snapshots:batchDelete",
                json=snapshot_data,
                headers=headers,
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to batch delete snapshots for filesystem '{filesystem}': {str(e)}"
        ) from e


async def get_snapdir_settings_api(
    filesystem: str,
    domain: Optional[str] = None,
) -> Any:
    """Get snapdir settings for a filesystem.

    Args:
        filesystem: Filesystem name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing snapdir settings

    Raises:
        StorageScaleAPIError: If the API request fails
    """
    headers = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.get(
                f"/scalemgmt/v3/filesystems/{filesystem}/snapshots:snapdir",
                headers=headers,
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to get snapdir settings for filesystem '{filesystem}': {str(e)}"
        ) from e
