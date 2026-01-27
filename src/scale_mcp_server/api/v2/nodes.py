"""IBM Storage Scale Node Health operations."""

from typing import Optional, Any, Dict
from scale_mcp_server.utils.client import StorageScaleClient, StorageScaleAPIError


async def get_node_health_states_api(
    name: str,
    fields: Optional[str] = None,
    filter: Optional[str] = None,
) -> Any:
    """Get System Health states for nodes.

    Args:
        name: Node name or ':all:' for all nodes
        fields: Comma-separated list of fields to return
        filter: Filter expression

    Returns:
        Dictionary containing node health states

    Raises:
        StorageScaleAPIError: If API call fails
    """
    query_params: Dict[str, Any] = {}
    if fields:
        query_params["fields"] = fields
    if filter:
        query_params["filter"] = filter

    try:
        async with StorageScaleClient(api_version="v2") as client:
            return await client.get(
                f"/scalemgmt/v2/nodes/{name}/health/states",
                params=query_params,
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to get health states for node '{name}': {str(e)}"
        ) from e


async def get_node_health_events_api(
    name: str,
    fields: Optional[str] = None,
    filter: Optional[str] = None,
) -> Any:
    """Get System Health events for a node or nodeclass.

    Returns a list of currently active System Health events for the given node or nodeclass.

    Args:
        name: Nodeclass, node name or ':all:'
        fields: Comma separated list of fields to be included in response. ':all:' selects all available fields
        filter: Filter objects by expression, e.g. 'status=HEALTHY,entityType=FILESET'

    Returns:
        Dictionary containing system health events information

    Raises:
        StorageScaleAPIError: If API call fails
    """
    params = {}
    if fields:
        params["fields"] = fields
    if filter:
        params["filter"] = filter

    try:
        async with StorageScaleClient(api_version="v2") as client:
            return await client.get(
                f"/scalemgmt/v2/nodes/{name}/health/events",
                params=params,
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to get health events for node '{name}': {str(e)}"
        ) from e
