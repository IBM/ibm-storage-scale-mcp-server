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
# Re-enable only after input validation and auth are reviewed and approved.

# @mcp.tool()
def apply_policy(filesystem: str) -> str:
    """Execute mmapplypolicy command to apply the ILM policy on a filesystem.

    Temporarily disabled pending security review.
    """
    raise NotImplementedError(
        "apply_policy is temporarily disabled pending a security review. "
        "See HackerOne report for details."
    )
