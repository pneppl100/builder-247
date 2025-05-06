"""Centralized logging configuration and utilities."""

import logging
import sys
import traceback
from typing import Any, Optional, Union
from pathlib import Path
from functools import wraps
import ast
from .errors import format_error

# Configure root logger to capture all log levels
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    handlers=[
        logging.StreamHandler(sys.stderr)
    ]
)

# Create our logger
logger = logging.getLogger("agent_framework")
logger.propagate = False

def configure_logging(log_level: int = logging.INFO) -> None:
    """
    Configure logging for the application with adjustable log level.

    Args:
        log_level: Logging level (default: logging.INFO)
    """
    logger.setLevel(log_level)


def log_advanced_error(
    error: Exception,
    context: Optional[Union[dict, str]] = None,
    include_traceback: bool = True,
    log_level: int = logging.ERROR
) -> None:
    """
    Advanced error logging with optional context and tracebacks.

    Args:
        error: The exception to log
        context: Additional context for the error
        include_traceback: Whether to include full stack trace
        log_level: Logging level for the error
    """
    # Convert string context to dictionary if needed
    if isinstance(context, str):
        context = {"message": context}

    # Format the error with context
    error_info = format_error(error, context, include_traceback)

    # Log error details
    logger.log(log_level, f"Error: {error_info['message']}")
    
    if context:
        logger.log(log_level, f"Context: {context}")
    
    if include_traceback:
        logger.log(log_level, f"Traceback:\n{error_info['traceback']}")


# Alias functions with default logging methods
log_section = logger.info
log_key_value = logger.info
log_value = logger.info
log_dict = log_key_value
log_error = log_advanced_error