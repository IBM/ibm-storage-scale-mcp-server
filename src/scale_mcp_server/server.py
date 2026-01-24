import argparse
from fastmcp import FastMCP
from pathlib import Path
from scale_mcp_server.utils.read_config import read_config, setup_logging
from scale_mcp_server.tools.v3 import (
    clusters,
    config,
    diagnostics,
    filesets,
    filesystems,
    nodes,
    nsds,
    policies,
    quotas,
    snapshots,
    storage_pools,
    version,
)
from scale_mcp_server.tools.v2 import (
    nodes_health,
    filesystems_health,
)


def main():
    parser = argparse.ArgumentParser(
        description="IBM Storage Scale MCP Server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run with HTTP transport on default port 8000 (localhost only)
  scale-mcp-server --transport http

  # Run with HTTP transport binding to all interfaces
  scale-mcp-server --transport http --host 0.0.0.0

  # Run with HTTP transport on custom port
  scale-mcp-server --transport http --port 3000

  # Run with stdio transport
  scale-mcp-server --transport stdio

  # Run with custom log level
  scale-mcp-server --transport http --port 8000 --log-level DEBUG
        """,
    )

    parser.add_argument(
        "--transport",
        type=str,
        choices=["stdio", "http"],
        default="http",
        help="Transport method to use: stdio or http (StreamableHTTP, default: http)",
    )

    parser.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
        help="Host address to bind to for http transport (default: 127.0.0.1). Use 0.0.0.0 to bind to all interfaces.",
    )

    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port number for http transport (default: 8000).",
    )

    parser.add_argument(
        "--log-level",
        type=str,
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="DEBUG",
        help="Log level for the MCP server (default: DEBUG).",
    )

    args = parser.parse_args()

    # Load configuration
    config_path = Path(__file__).parent.parent.parent / "config" / "mcp_config.ini"
    config_data = read_config(config_path=config_path)
    setup_logging(config_data)

    # Initialize MCP server
    mcp = FastMCP(name="scale-mcp-server", version="1.0.0")

    # Mounting sub-servers
    mcp.mount(clusters.mcp)
    mcp.mount(config.mcp)
    mcp.mount(diagnostics.mcp)
    mcp.mount(filesets.mcp)
    mcp.mount(filesystems.mcp)
    mcp.mount(nodes.mcp)
    mcp.mount(nsds.mcp)
    mcp.mount(policies.mcp)
    mcp.mount(quotas.mcp)
    mcp.mount(snapshots.mcp)
    mcp.mount(storage_pools.mcp)
    mcp.mount(version.mcp)
    # V2
    mcp.mount(nodes_health.mcp)
    mcp.mount(filesystems_health.mcp)

    fastmcp_config = config_data.get("fastmcp", {})
    log_level = (
        args.log_level if args.log_level else fastmcp_config.get("level", "INFO")
    )

    run_kwargs = {"transport": args.transport, "log_level": log_level}

    # Host and port are valid for http transport
    if args.transport == "http":
        run_kwargs["host"] = args.host
        run_kwargs["port"] = args.port

    # Run the MCP server
    mcp.run(**run_kwargs)
