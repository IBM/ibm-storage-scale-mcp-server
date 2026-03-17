#!/usr/bin/env python3
"""Script to list all available MCP tools from IBM Storage Scale MCP Server.

This script can:
1. Connect to an already running HTTP server and list its tools
2. Launch a temporary stdio server instance to inspect its tools

For stdio: This launches a NEW server process (like mcp-inspector does)
For HTTP: This connects to an ALREADY RUNNING server instance
"""

import asyncio
import argparse
import json
import sys
from typing import Any

try:
    from fastmcp.client import Client
    from fastmcp.client.transports.stdio import StdioTransport
    from fastmcp.client.transports.http import StreamableHttpTransport
except ImportError:
    print("Error: fastmcp package not found. Install it with: pip install fastmcp")
    sys.exit(1)


async def list_tools_stdio(filesystem_paths: list[str] | None = None) -> list[dict[str, Any]]:
    """Launch a temporary MCP server via stdio and list all tools.
    
    Note: This launches a NEW server process to inspect its tools.
    It does NOT connect to an already running stdio server.
    
    Args:
        filesystem_paths: Optional list of filesystem paths to enable file operations tools
    
    Returns:
        List of tool information dictionaries
    """
    # Create stdio transport - this will launch a new server process
    args = ["--transport", "stdio"]
    if filesystem_paths:
        args.extend(["--filesystem-paths"] + filesystem_paths)
    
    transport = StdioTransport(
        command="scale-mcp-server",
        args=args,
    )
    
    tools = []
    
    # Connect to the server
    async with Client(transport) as client:
        # List all available tools
        tools_list = await client.list_tools()
        
        for tool in tools_list:
            tool_info = {
                'name': tool.name,
                'description': tool.description or 'No description available',
            }
            
            # Extract input schema if available
            if hasattr(tool, 'inputSchema') and tool.inputSchema:
                tool_info['input_schema'] = tool.inputSchema
            
            tools.append(tool_info)
    
    return tools


async def list_tools_http(host: str = "127.0.0.1", port: int = 8000) -> list[dict[str, Any]]:
    """Connect to MCP server via HTTP and list all tools.
    
    Args:
        host: Server host address
        port: Server port number
        
    Returns:
        List of tool information dictionaries
    """
    url = f"http://{host}:{port}/mcp"
    transport = StreamableHttpTransport(url)
    
    tools = []
    
    # Connect to the server
    async with Client(transport) as client:
        # List all available tools
        tools_list = await client.list_tools()
        
        for tool in tools_list:
            tool_info = {
                'name': tool.name,
                'description': tool.description or 'No description available',
            }
            
            # Extract input schema if available
            if hasattr(tool, 'inputSchema') and tool.inputSchema:
                tool_info['input_schema'] = tool.inputSchema
            
            tools.append(tool_info)
    
    return tools


def print_tools_summary(tools: list[dict[str, Any]]) -> None:
    """Print a formatted summary of all tools.
    
    Args:
        tools: List of tool information dictionaries
    """
    print("=" * 80)
    print("IBM Storage Scale MCP Server - Available Tools")
    print("=" * 80)
    print(f"\nTotal Tools: {len(tools)}\n")
    
    for i, tool in enumerate(sorted(tools, key=lambda x: x['name']), 1):
        print(f"{i}. {tool['name']}")
        
        # Print description (first line only for summary)
        desc = tool['description'].strip().split('\n')[0] if tool['description'] else 'No description'
        print(f"   {desc}")
        
        # Print parameters if available
        if 'input_schema' in tool:
            schema = tool['input_schema']
            if isinstance(schema, dict) and 'properties' in schema:
                params = schema['properties']
                required = schema.get('required', [])
                print(f"   Parameters: {len(params)}")
                for param_name in sorted(params.keys()):
                    req_marker = " (required)" if param_name in required else ""
                    print(f"     - {param_name}{req_marker}")
        print()
    
    print(f"{'=' * 80}\n")


def print_tools_detailed(tools: list[dict[str, Any]]) -> None:
    """Print detailed information about all tools.
    
    Args:
        tools: List of tool information dictionaries
    """
    print("=" * 80)
    print("IBM Storage Scale MCP Server - Detailed Tool Information")
    print("=" * 80)
    
    for i, tool in enumerate(sorted(tools, key=lambda x: x['name']), 1):
        print(f"\n{i}. {tool['name']}")
        print("-" * 80)
        print(f"Description:\n{tool['description']}\n")
        
        if 'input_schema' in tool:
            schema = tool['input_schema']
            if isinstance(schema, dict) and 'properties' in schema:
                print("Parameters:")
                params = schema['properties']
                required = schema.get('required', [])
                
                for param_name in sorted(params.keys()):
                    param_info = params[param_name]
                    req_marker = " (required)" if param_name in required else " (optional)"
                    param_type = param_info.get('type', 'unknown')
                    param_desc = param_info.get('description', 'No description')
                    
                    print(f"  - {param_name}{req_marker}")
                    print(f"    Type: {param_type}")
                    print(f"    Description: {param_desc}")
                    
                    # Print enum values if available
                    if 'enum' in param_info:
                        print(f"    Allowed values: {', '.join(param_info['enum'])}")
                    
                    # Print default value if available
                    if 'default' in param_info:
                        print(f"    Default: {param_info['default']}")
                    
                    print()
            else:
                print("Parameters: None\n")
        else:
            print("Parameters: None\n")


async def main():
    """Main function to list all MCP tools from a running server."""
    parser = argparse.ArgumentParser(
        description="List all available MCP tools from IBM Storage Scale MCP Server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Launch temporary stdio server and list tools
  python list_tools.py --transport stdio

  # Connect to running HTTP server and list tools (default)
  python list_tools.py --transport http

  # List tools with detailed information
  python list_tools.py --detailed

  # Connect to custom HTTP endpoint
  python list_tools.py --transport http --host 0.0.0.0 --port 3000

  # Output as JSON
  python list_tools.py --format json

Transport Notes:
  stdio: Launches a NEW temporary server process to inspect tools
  http:  Connects to an ALREADY RUNNING server instance

For HTTP, start the server first:
  scale-mcp-server --transport http --port 8000
        """
    )
    
    parser.add_argument(
        '--transport',
        choices=['stdio', 'http'],
        default='http',
        help='Transport method to connect to the server (default: http)'
    )
    parser.add_argument(
        '--host',
        default='127.0.0.1',
        help='Server host address for HTTP transport (default: 127.0.0.1)'
    )
    parser.add_argument(
        '--port',
        type=int,
        default=8000,
        help='Server port for HTTP transport (default: 8000)'
    )
    parser.add_argument(
        '--detailed',
        action='store_true',
        help='Show detailed information including full descriptions and parameters'
    )
    parser.add_argument(
        '--format',
        choices=['text', 'json'],
        default='text',
        help='Output format (default: text)'
    )
    parser.add_argument(
        '--filesystem-paths',
        nargs='+',
        help='Filesystem paths to enable file operations tools (space-separated). '
             'Example: --filesystem-paths /data /home/user'
    )
    
    args = parser.parse_args()
    
    try:
        # Connect to the server and retrieve tools
        if args.transport == 'stdio':
            print("Launching temporary MCP server via stdio...\n")
            if args.filesystem_paths:
                print(f"Including filesystem tools for paths: {', '.join(args.filesystem_paths)}\n")
            tools = await list_tools_stdio(args.filesystem_paths)
        else:
            print(f"Connecting to MCP server at http://{args.host}:{args.port}/mcp...\n")
            tools = await list_tools_http(args.host, args.port)
        
        # Output based on format
        if args.format == 'json':
            print(json.dumps(tools, indent=2))
        else:
            if args.detailed:
                print_tools_detailed(tools)
            else:
                print_tools_summary(tools)
                
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if args.transport == 'stdio':
            print("\nMake sure 'scale-mcp-server' command is available in your PATH", file=sys.stderr)
            print("Or the server package is properly installed", file=sys.stderr)
        else:
            print("\nMake sure the MCP server is running with HTTP transport:", file=sys.stderr)
            print(f"  scale-mcp-server --transport http --host {args.host} --port {args.port}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
