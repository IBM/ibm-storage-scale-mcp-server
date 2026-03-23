"""CLI Command Executor for IBM Storage Scale MCP Server.

This module provides command execution capabilities with timeout controls.
Commands are limited by the tools that use them.
"""

import subprocess
from typing import Optional
import logging

logger = logging.getLogger(__name__)


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
        logger.debug(f"CommandExecutor initialized with timeout: {command_timeout}s")

    def run_command(
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
            subprocess.CompletedProcess with stdout, stderr, and returncode
            
        Raises:
            CommandTimeoutError: If command exceeds timeout
            CommandExecutionError: If command execution fails
        """
        try:
            logger.info(f"Executing command: {command}")
            result = subprocess.run(
                command,
                shell=shell,
                text=True,
                capture_output=True,
                timeout=self.command_timeout,
                cwd=cwd,
            )
            
            if result.returncode == 0:
                logger.info(f"Command executed successfully")
            else:
                logger.warning(f"Command failed with exit code {result.returncode}")
            
            return result
            
        except subprocess.TimeoutExpired:
            raise CommandTimeoutError(
                f"Command timed out after {self.command_timeout} seconds"
            )
        except Exception as e:
            raise CommandExecutionError(f"Command execution failed: {str(e)}")

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        pass
