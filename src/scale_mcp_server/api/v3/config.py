"""IBM Storage Scale Configuration operations."""

from typing import Optional, Any
from scale_mcp_server.utils.client import StorageScaleClient, StorageScaleAPIError


async def get_admin_config_api(
    domain: Optional[str] = None,
) -> Any:
    """Get admin configuration.

    Args:
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing admin configuration

    Raises:
        StorageScaleAPIError: If the API request fails
    """
    headers = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.get("/scalemgmt/v3/config/admin", headers=headers)
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to get admin configuration: {str(e)}"
        ) from e


async def update_admin_config_api(
    config_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Batch update admin configuration.

    Args:
        config_data: Configuration data (BatchUpdateAdminConfigRequest)
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing updated configuration

    Raises:
        StorageScaleAPIError: If the API request fails
    """
    headers = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.patch(
                "/scalemgmt/v3/config/admin:batchUpdate",
                json=config_data,
                headers=headers,
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to update admin configuration: {str(e)}"
        ) from e
