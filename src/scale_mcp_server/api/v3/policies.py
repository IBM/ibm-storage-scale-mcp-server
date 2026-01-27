"""IBM Storage Scale Policy operations."""

from typing import Optional, Any
from scale_mcp_server.utils.client import StorageScaleClient, StorageScaleAPIError


async def get_policy_api(
    filesystem: str,
    domain: Optional[str] = None,
) -> Any:
    """Get policy for a filesystem.

    Args:
        filesystem: Filesystem name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing policy information

    Raises:
        StorageScaleAPIError: If the API request fails
    """
    headers = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.get(
                f"/scalemgmt/v3/filesystems/{filesystem}/policy", headers=headers
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to get policy for filesystem '{filesystem}': {str(e)}"
        ) from e


async def update_policy_api(
    filesystem: str,
    policy_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Update policy for a filesystem.

    Args:
        filesystem: Filesystem name
        policy_data: Policy configuration data
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing updated policy information

    Raises:
        StorageScaleAPIError: If the API request fails
    """
    headers = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.patch(
                f"/scalemgmt/v3/filesystems/{filesystem}/policy",
                json=policy_data,
                headers=headers,
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to update policy for filesystem '{filesystem}': {str(e)}"
        ) from e
