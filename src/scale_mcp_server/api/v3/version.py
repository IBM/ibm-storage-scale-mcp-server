"""IBM Storage Scale Version operations."""

from typing import Optional, Any, Dict
from scale_mcp_server.utils.client import StorageScaleClient, StorageScaleAPIError


async def get_version_api(
    domain: Optional[str] = None,
) -> Any:
    """Get IBM Storage Scale version information.

    Args:
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing version information

    Raises:
        StorageScaleAPIError: If API call fails
    """
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.get("/scalemgmt/v3/version", headers=headers)
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to get version information: {str(e)}"
        ) from e
