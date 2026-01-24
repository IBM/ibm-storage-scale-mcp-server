"""IBM Storage Scale Filesystem Health operations."""

from typing import Any
from scale_mcp_server.utils.client import StorageScaleClient, StorageScaleAPIError


async def get_filesystem_health_states_api(
    filesystem: str,
) -> Any:
    """Get Cluster Related health State for a filesystem.

    Args:
        filesystem: Filesystem name

    Returns:
        Dictionary containing filesystem health state

    Raises:
        StorageScaleAPIError: If API call fails
    """
    try:
        async with StorageScaleClient(api_version="v2") as client:
            return await client.get(
                f"/scalemgmt/v2/cluster/filesystems/{filesystem}/health/state",
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to get health state for filesystem '{filesystem}': {str(e)}"
        ) from e


async def get_filesystem_health_events_api(
    filesystem_name: str,
) -> Any:
    """Get Cluster Related System Health events for a filesystem.

    Returns a list of currently active Cluster related System Health events for the specified filesystem.

    Args:
        filesystem_name: Filesystem name

    Returns:
        Dictionary containing filesystem health events information

    Raises:
        StorageScaleAPIError: If API call fails
    """
    try:
        async with StorageScaleClient(api_version="v2") as client:
            return await client.get(
                f"/scalemgmt/v2/cluster/filesystems/{filesystem_name}/health/events",
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to get health events for filesystem '{filesystem_name}': {str(e)}"
        ) from e
