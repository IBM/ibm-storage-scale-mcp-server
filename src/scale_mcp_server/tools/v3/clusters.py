"""IBM Storage Scale Cluster Management MCP Server."""

from typing import Optional, Literal, Any
from fastmcp import FastMCP, Context
from scale_mcp_server.api.v3.clusters import (
    list_clusters_api,
    list_remote_clusters_api,
    get_remote_cluster_api,
    list_cluster_trust_api,
)


# Create the clusters MCP server
mcp = FastMCP("clusters", instructions="Cluster management operations")


@mcp.tool()
async def list_clusters(
    ctx: Context,
    view: Optional[Literal["BASIC", "CES", "CNFS", "NODE_COMMENTS"]] = None,
    domain: Optional[str] = None,
) -> Any:
    """List all Storage Scale clusters.

    Args:
        view: Level of detail to return (BASIC, CES, CNFS, NODE_COMMENTS)
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing cluster information
    """
    await ctx.info(f"Tool called: list_clusters with view={view}, domain={domain}")

    try:
        await ctx.debug("Making API request to /scalemgmt/v3/clusters")
        result = await list_clusters_api(view=view, domain=domain)
        await ctx.info("Successfully retrieved cluster information")
        return result

    except Exception as e:
        await ctx.error(f"Failed to list clusters: {str(e)}")
        raise


@mcp.tool()
async def list_remote_clusters(
    ctx: Context,
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
    """
    await ctx.info("Tool called: list_remote_clusters")
    await ctx.debug(f"Listing remote clusters with page_size={page_size}, view={view}")

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
        await ctx.debug("Making API request to /scalemgmt/v3/clusters/remote")
        result = await list_remote_clusters_api(
            page_size=page_size, page_token=page_token, view=view, domain=domain
        )
        await ctx.info("Successfully retrieved remote clusters information")
        return result

    except Exception as e:
        await ctx.error(f"Failed to list remote clusters: {str(e)}")
        raise


@mcp.tool()
async def get_remote_cluster(
    ctx: Context,
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
    """
    await ctx.info(f"Tool called: get_remote_cluster with name={name}")
    await ctx.debug(f"Retrieving information for remote cluster: {name}")

    query_params = {}
    if view:
        query_params["view"] = view

    headers = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        await ctx.debug("Making API request to /scalemgmt/v3/clusters/remote")
        result = await get_remote_cluster_api(name=name, view=view, domain=domain)
        await ctx.info(f"Successfully retrieved remote cluster: {name}")
        return result

    except Exception as e:
        await ctx.error(f"Failed to get remote cluster {name}: {str(e)}")
        raise


@mcp.tool()
async def list_cluster_trust(
    ctx: Context,
    end_point: Optional[str] = None,
    domain: Optional[str] = None,
) -> Any:
    """List cluster trust information.

    Args:
        end_point: Endpoint to filter by
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing cluster trust information
    """
    await ctx.info("Tool called: list_cluster_trust")
    await ctx.debug(f"Listing cluster trust information, end_point={end_point}")

    query_params = {}
    if end_point:
        query_params["end_point"] = end_point

    headers = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        await ctx.debug(
            "Making API request to /scalemgmt/v3/clusters/remote/authorized"
        )
        result = await list_cluster_trust_api(end_point=end_point, domain=domain)
        await ctx.info("Successfully retrieved cluster trust information")
        return result

    except Exception as e:
        await ctx.error(f"Failed to list cluster trust: {str(e)}")
        raise
