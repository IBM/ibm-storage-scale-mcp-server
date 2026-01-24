"""IBM Storage Scale NSD operations."""

from typing import Optional, Any
from scale_mcp_server.utils.client import StorageScaleClient, StorageScaleAPIError


async def list_nsds_api(
    domain: Optional[str] = None,
) -> Any:
    """List all NSDs (Network Shared Disks).

    Args:
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing NSDs information

    Raises:
        StorageScaleAPIError: If the API request fails
    """
    headers = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.get("/scalemgmt/v3/nsds", headers=headers)
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to list NSDs: {str(e)}") from e


async def get_nsd_api(
    nsd_name: str,
    domain: Optional[str] = None,
) -> Any:
    """Get information about a specific NSD.

    Args:
        nsd_name: NSD name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing NSD information

    Raises:
        StorageScaleAPIError: If the API request fails
    """
    headers = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.get(f"/scalemgmt/v3/nsds/{nsd_name}", headers=headers)
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to get NSD '{nsd_name}': {str(e)}") from e


async def batch_create_nsds_api(
    nsds_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Create multiple NSDs.

    Args:
        nsds_data: Batch NSD creation data
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
                "/scalemgmt/v3/nsds:batchCreate", json=nsds_data, headers=headers
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to batch create NSDs: {str(e)}") from e


async def batch_delete_nsds_api(
    nsds_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Delete multiple NSDs.

    Args:
        nsds_data: Batch NSD deletion data
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
                "/scalemgmt/v3/nsds:batchDelete", json=nsds_data, headers=headers
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to batch delete NSDs: {str(e)}") from e
