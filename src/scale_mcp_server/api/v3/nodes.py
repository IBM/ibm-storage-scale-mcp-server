"""IBM Storage Scale Node operations."""

from typing import Optional, Any
from scale_mcp_server.utils.client import StorageScaleClient, StorageScaleAPIError


async def add_node_api(
    node_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Add a new node to the cluster.

    Args:
        node_data: Node configuration data
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing node information

    Raises:
        StorageScaleAPIError: If the API request fails
    """
    headers = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.post(
                "/scalemgmt/v3/nodes", json=node_data, headers=headers
            )
    except StorageScaleAPIError as e:
        node_name = node_data.get("name", "unknown")
        raise StorageScaleAPIError(f"Failed to add node '{node_name}': {str(e)}") from e


async def batch_add_nodes_api(
    nodes_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Add multiple nodes to the cluster.

    Args:
        nodes_data: Batch node configuration data
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing operation status

    Raises:
        StorageScaleAPIError: If the API request fails
    """
    headers = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.post(
                "/scalemgmt/v3/nodes:batchAdd", json=nodes_data, headers=headers
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to batch add nodes: {str(e)}") from e


async def get_nodes_config_api(
    domain: Optional[str] = None,
) -> Any:
    """Get configuration of all nodes.

    Args:
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing nodes configuration

    Raises:
        StorageScaleAPIError: If the API request fails
    """
    headers = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.get("/scalemgmt/v3/nodes/config", headers=headers)
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to get nodes configuration: {str(e)}"
        ) from e


async def get_nodes_status_api(
    domain: Optional[str] = None,
) -> Any:
    """Get status of all nodes.

    Args:
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing nodes status

    Raises:
        StorageScaleAPIError: If the API request fails
    """
    headers = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.get("/scalemgmt/v3/nodes/status", headers=headers)
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to get nodes status: {str(e)}") from e


async def start_nodes_api(
    nodes_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Start specified nodes.

    Args:
        nodes_data: Data specifying which nodes to start
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing operation status

    Raises:
        StorageScaleAPIError: If the API request fails
    """
    headers = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.post(
                "/scalemgmt/v3/nodes:start", json=nodes_data, headers=headers
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to start nodes: {str(e)}") from e


async def stop_nodes_api(
    nodes_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Stop specified nodes.

    Args:
        nodes_data: Data specifying which nodes to stop
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing operation status

    Raises:
        StorageScaleAPIError: If the API request fails
    """
    headers = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.post(
                "/scalemgmt/v3/nodes:stop", json=nodes_data, headers=headers
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to stop nodes: {str(e)}") from e


async def get_node_version_api(
    node: str,
    domain: Optional[str] = None,
) -> Any:
    """Get version information for a specific node.

    Args:
        node: Node name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing node version information

    Raises:
        StorageScaleAPIError: If the API request fails
    """
    headers = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.get(
                f"/scalemgmt/v3/nodes/{node}/diagnostics/version", headers=headers
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to get version for node '{node}': {str(e)}"
        ) from e
