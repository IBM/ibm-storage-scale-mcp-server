"""IBM Storage Scale Cluster operations."""

from typing import Optional, Literal, Any, Dict
from scale_mcp_server.utils.client import StorageScaleClient, StorageScaleAPIError


async def list_clusters_api(
    view: Optional[Literal["BASIC", "CES", "CNFS", "NODE_COMMENTS"]] = None,
    domain: Optional[str] = None,
) -> Any:
    """List all Storage Scale clusters.

    Args:
        view: Level of detail to return (BASIC, CES, CNFS, NODE_COMMENTS)
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing cluster information

    Raises:
        StorageScaleAPIError: If API call fails
    """
    query_params: Dict[str, Any] = {}
    if view:
        query_params["view"] = view

    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.get(
                "/scalemgmt/v3/clusters", params=query_params, headers=headers
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to list clusters: {str(e)}") from e


async def list_remote_clusters_api(
    page_size: Optional[int] = None,
    page_token: Optional[str] = None,
    view: Optional[Literal["REMOTE_BASIC", "FULL"]] = None,
    domain: Optional[str] = None,
) -> Any:
    """List remote clusters information.

    Args:
        page_size: Number of results per page
        page_token: Token for pagination
        view: Level of detail (REMOTE_BASIC, FULL)
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing remote clusters information

    Raises:
        StorageScaleAPIError: If API call fails
    """
    query_params = {}
    if page_size:
        query_params["page_size"] = page_size
    if page_token:
        query_params["page_token"] = page_token
    if view:
        query_params["view"] = view

    headers = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.get(
                "/scalemgmt/v3/clusters/remote", params=query_params, headers=headers
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to list remote clusters: {str(e)}") from e


async def get_remote_cluster_api(
    name: str,
    view: Optional[Literal["REMOTE_BASIC", "FULL"]] = None,
    domain: Optional[str] = None,
) -> Any:
    """Get information of a remote cluster.

    Args:
        name: Name of the remote cluster
        view: Level of detail (REMOTE_BASIC, FULL)
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing remote cluster information

    Raises:
        StorageScaleAPIError: If API call fails
    """
    query_params = {}
    if view:
        query_params["view"] = view

    headers = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.get(
                f"/scalemgmt/v3/clusters/remote/{name}",
                params=query_params,
                headers=headers,
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to get remote cluster '{name}': {str(e)}"
        ) from e


async def list_cluster_trust_api(
    end_point: Optional[str] = None,
    domain: Optional[str] = None,
) -> Any:
    """List cluster trust information.

    Args:
        end_point: Endpoint to filter by
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing cluster trust information

    Raises:
        StorageScaleAPIError: If API call fails
    """
    query_params = {}
    if end_point:
        query_params["end_point"] = end_point

    headers = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.get(
                "/scalemgmt/v3/clusters/trust", params=query_params, headers=headers
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to list cluster trust information: {str(e)}"
        ) from e
