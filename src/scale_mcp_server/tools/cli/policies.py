"""IBM Storage Scale CLI Policy Tools."""

from fastmcp import FastMCP
import logging
from pathlib import Path
import os
import json

from scale_mcp_server.adapters.ssh_executor import SSHCommandExecutor
from scale_mcp_server.adapters.base import CommandError
from scale_mcp_server.utils.read_config import read_config
from scale_mcp_server.utils.helpers import clean_output

logger = logging.getLogger(__name__)

# Create the CLI MCP server
mcp = FastMCP("scale-cli", instructions="IBM Storage Scale CLI command operations via SSH")

# Load configuration from default location
config_path = Path(__file__).resolve().parents[4] / "config" / "scale_config.ini"
config = read_config(config_path)

# Get SSH connection details from config
if 'ssh' not in config:
    raise ValueError("Missing [ssh] section in configuration file")

ssh_config = config['ssh']
if not ssh_config.get('hostname'):
    raise ValueError("Missing 'hostname' in [ssh] configuration")
if not ssh_config.get('username'):
    raise ValueError("Missing 'username' in [ssh] configuration")

SSH_HOST = ssh_config['hostname']
SSH_PORT = int(ssh_config.get('port', 22))
SSH_USERNAME = ssh_config['username']
SSH_PASSWORD = ssh_config.get('password') or None
SSH_KEY_PATH = ssh_config.get('key_path') or None

# Expand ~ to home directory if present in key path
if SSH_KEY_PATH:
    SSH_KEY_PATH = os.path.expanduser(SSH_KEY_PATH)

# Get timeout from config, default to 5.0 seconds (same as HTTP API)
COMMAND_TIMEOUT = int(float(config.get('scale_api', {}).get('timeout', 5.0)))


# TEMPORARILY DISABLED — HackerOne command injection report.
# The filesystem argument was passed unsanitised into an SSH exec_command
# string, allowing shell metacharacters to run arbitrary commands on the
# cluster. The @mcp.tool() decorator is commented out so FastMCP does not
# register this function — it cannot be called via tools/call at all.
#
# To re-enable once security review is complete:
#   1. Uncomment @mcp.tool() below
#   2. Remove the NotImplementedError block
#   3. Uncomment the original implementation block

# @mcp.tool()
def apply_policy(filesystem: str) -> str:
    """Execute mmapplypolicy command to apply the ILM policy on a filesystem.

    This command applies the policy that was provided.
    It extracts the policy from filesystem metadata and executes it.

    Args:
        filesystem: The filesystem name (e.g., 'fs1')

    Returns:
        str: Command output and execution status
    """
    # --- DISABLED: remove this block when re-enabling ---
    raise NotImplementedError(
        "apply_policy is temporarily disabled pending a security review. "
        "See HackerOne report for details."
    )

    # --- Original implementation — uncomment to restore ---
    # try:
    #     # Create SSH executor with configured timeout
    #     executor = SSHCommandExecutor(
    #         host=SSH_HOST,
    #         username=SSH_USERNAME,
    #         password=SSH_PASSWORD if not SSH_KEY_PATH else None,
    #         key_filename=SSH_KEY_PATH,
    #         port=SSH_PORT,
    #         command_timeout=COMMAND_TIMEOUT
    #     )
    #
    #     # Execute mmapplypolicy directly without extracting policy to file
    #     command = ["mmapplypolicy", filesystem, "-I", "yes"]
    #     logger.info(f"Running policy on filesystem '{filesystem}'")
    #
    #     # Execute via SSH using context manager
    #     with executor:
    #         result = executor.execute(command)
    #
    #     # Return structured JSON response for agent consumption
    #     response = {
    #         "status": "success" if result.success else "failed",
    #         "filesystem": filesystem,
    #         "exit_code": result.returncode,
    #         "output": clean_output(result.stdout),
    #         "error": clean_output(result.stderr) if not result.success else None
    #     }
    #
    #     if not result.success:
    #         raise CommandError(json.dumps(response))
    #
    #     return json.dumps(response)
    #
    # except CommandError as e:
    #     logger.error(f"Failed to execute policy: {str(e)}")
    #     raise
    # except Exception as e:
    #     logger.error(f"Unexpected error: {str(e)}")
    #     raise
