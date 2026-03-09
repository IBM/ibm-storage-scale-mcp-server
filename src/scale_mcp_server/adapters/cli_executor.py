"""CLI Command Executor for IBM Storage Scale MCP Server.

This module provides command execution capabilities with timeout controls.
Commands are limited by the tools that use them.
"""

import subprocess
from typing import Optional


class CommandError(Exception):
    """Base exception for command-related errors"""
    pass


class CommandExecutionError(CommandError):
    """Command execution errors"""
    pass


class CommandTimeoutError(CommandError):
    """Command timeout errors"""
    pass


class CommandExecutor:
    """Command executor with timeout controls."""
    
    def __init__(self, command_timeout: int = 30):
        """Initialize the command executor.
        
        Args:
            command_timeout: Maximum execution time in seconds (default: 30)
        """
        self.command_timeout = command_timeout

    def execute(
        self, 
        command: list[str], 
        shell: bool = False,
        cwd: Optional[str] = None
    ) -> subprocess.CompletedProcess:
        """Execute a command in a controlled environment.
        
        Args:
            command: Command and arguments as a list (e.g., ['mmlsfs', 'all'])
            shell: Whether to execute through shell (default: False)
            cwd: Working directory (optional)
            
        Returns:
            subprocess.CompletedProcess: The result of the command execution
            
        Raises:
            CommandTimeoutError: If command exceeds timeout
            CommandExecutionError: If command execution fails
        """
        try:
            return subprocess.run(
                command,
                shell=shell,
                text=True,
                capture_output=True,
                timeout=self.command_timeout,
                cwd=cwd,
            )
        except subprocess.TimeoutExpired:
            raise CommandTimeoutError(
                f"Command timed out after {self.command_timeout} seconds"
            )
        except Exception as e:
            raise CommandExecutionError(f"Command execution failed: {str(e)}")
