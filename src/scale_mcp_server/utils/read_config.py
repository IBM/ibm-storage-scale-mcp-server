import configparser
import logging
import sys
from pathlib import Path
from typing import Dict, Any
from logging.handlers import RotatingFileHandler


def read_config(config_path: Path) -> Dict[str, Any]:
    """Read specified configuration file.

    Returns:
        Dictionary containing configuration settings
    """
    if not config_path.is_file():
        print(f"Config file '{config_path}' does not exist.")
        sys.exit(1)

    config = configparser.ConfigParser()
    config.read(config_path)

    return {section: dict(config[section]) for section in config.sections()}


def setup_logging(config: Dict[str, Any]) -> None:
    """Setup logging based on MCP configuration.

    Args:
        config: Optional configuration dictionary.
    """
    logging_config = config.get("logging", {})
    log_level_str = logging_config.get("level", "INFO").upper()
    log_level = getattr(logging, log_level_str, logging.INFO)
    log_format = logging_config.get("format", "json")

    # Setup formatter based on format type
    if log_format == "json":
        formatter = logging.Formatter(
            '{"time":"%(asctime)s","name":"%(name)s","level":"%(levelname)s","message":"%(message)s"}'
        )
    else:
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

    # Setup root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Clear existing handlers
    root_logger.handlers.clear()

    # Setup console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # Setup file handler if file path is configured
    file_path = logging_config.get("file_path")
    if file_path:
        path_obj = Path(file_path)

        # Create logs directory if it doesn't exist
        path_obj.parent.mkdir(parents=True, exist_ok=True)

        # Parse file_max_size from config (e.g., "10MB" -> 10485760 bytes)
        max_size_str = logging_config.get("file_max_size", "10MB")
        if max_size_str.upper().endswith("MB"):
            max_bytes = int(max_size_str[:-2]) * 1024 * 1024
        elif max_size_str.upper().endswith("KB"):
            max_bytes = int(max_size_str[:-2]) * 1024
        else:
            max_bytes = int(max_size_str)

        # Get file_max_files from config
        max_files = int(logging_config.get("file_max_files", "5"))

        file_handler = RotatingFileHandler(
            file_path,
            maxBytes=max_bytes,
            backupCount=max_files,
        )
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
