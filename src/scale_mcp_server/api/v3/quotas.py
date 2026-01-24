"""IBM Storage Scale Quota operations."""

from typing import Optional, Any
from scale_mcp_server.utils.client import StorageScaleClient, StorageScaleAPIError


async def list_quotas_api(
    filesystem: str,
    domain: Optional[str] = None,
) -> Any:
    """List all quotas for a filesystem.

    Args:
        filesystem: Filesystem name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing quotas information

    Raises:
        StorageScaleAPIError: If the API request fails
    """
    headers = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.get(
                f"/scalemgmt/v3/filesystems/{filesystem}/quotas", headers=headers
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to list quotas for filesystem '{filesystem}': {str(e)}"
        ) from e


async def set_quota_api(
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

    Raises:
        StorageScaleAPIError: If the API request fails
    """
    headers = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.put(
                f"/scalemgmt/v3/filesystems/{filesystem}/quotas",
                json=quota_data,
                headers=headers,
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to set quota for filesystem '{filesystem}': {str(e)}"
        ) from e
