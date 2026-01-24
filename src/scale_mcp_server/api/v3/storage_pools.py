"""IBM Storage Scale Storage Pool operations."""

from typing import Optional, Any
from scale_mcp_server.utils.client import StorageScaleClient, StorageScaleAPIError


async def list_storage_pools_api(
    filesystem: str,
    domain: Optional[str] = None,
) -> Any:
    """List storage pools for a filesystem.

    Args:
        filesystem: Filesystem name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing storage pools information

    Raises:
        StorageScaleAPIError: If the API request fails
    """
    headers = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.get(
                f"/scalemgmt/v3/filesystems/{filesystem}/storagepools", headers=headers
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to list storage pools for filesystem '{filesystem}': {str(e)}"
        ) from e


async def get_storage_pool_api(
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

    Raises:
        StorageScaleAPIError: If the API request fails
    """
    headers = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.get(
                f"/scalemgmt/v3/filesystems/{filesystem}/storagepools/{pool_name}",
                headers=headers,
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to get storage pool '{pool_name}' for filesystem '{filesystem}': {str(e)}"
        ) from e
