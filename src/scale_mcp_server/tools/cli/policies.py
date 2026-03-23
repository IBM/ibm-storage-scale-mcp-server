"""IBM Storage Scale CLI Command Tools."""

from fastmcp import FastMCP
import logging

from scale_mcp_server.adapters.cli_executor import CommandExecutor, CommandError
from scale_mcp_server.utils.helpers import clean_output

logger = logging.getLogger(__name__)

# Create the CLI MCP server
mcp = FastMCP("scale-cli", instructions="IBM Storage Scale CLI command operations (local execution)")


@mcp.tool()
def apply_policy(filesystem: str) -> str:
    """Apply ILM policy to a filesystem using mmapplypolicy command.

    Args:
        filesystem: Filesystem name

    Returns:
        Command execution status and output
    """
    try:
        executor = CommandExecutor(command_timeout=300)
        command = ["mmapplypolicy", filesystem, "-I", "yes"]
        logger.info(f"Running policy on filesystem '{filesystem}'")

        # Execute command
        result = executor.run_command(command)
        stdout = result.stdout
        stderr = result.stderr
        exit_code = result.returncode

        if exit_code == 0:
            return clean_output(stdout)
        else:
            return clean_output(stderr) if stderr else clean_output(stdout)

    except CommandError as e:
        error_msg = f"Failed to execute policy: {str(e)}"
        logger.error(error_msg)
        return f"{error_msg}"
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        logger.error(error_msg)
        return f"{error_msg}"
