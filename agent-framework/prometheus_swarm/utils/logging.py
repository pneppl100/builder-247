"""Centralized logging configuration and utilities."""

import logging
import sys
import traceback
from typing import Any, Optional, Union
from pathlib import Path
from functools import wraps
import ast
from colorama import init, Fore, Style
from .errors import format_error

# Initialize colorama for cross-platform color support
init(strip=False)  # Force color output even when not in a terminal

# Create our logger
logger = logging.getLogger("agent_framework")
logger.setLevel(logging.INFO)
# Prevent propagation to avoid duplicate logs
logger.propagate = False

# Track if logging has been configured
_logging_configured = False


class SectionFormatter(logging.Formatter):
    """Custom formatter with enhanced color and section handling."""

    def format(self, record):
        # Color and format logic remains the same as before
        base_msg = super().format(record)
        # Ensure colorized errors appear
        if record.levelno >= logging.ERROR:
            base_msg = f"{Fore.RED}{base_msg}{Style.RESET_ALL}"
        return base_msg


def configure_logging(log_level: int = logging.INFO) -> None:
    """
    Configure logging for the application with adjustable log level.

    Args:
        log_level: Logging level (default: logging.INFO)
    """
    global _logging_configured
    logger.handlers.clear()  # Ensure clean logging setup

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_formatter = logging.Formatter('%(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    logger.setLevel(log_level)

    _logging_configured = True


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
    if not _logging_configured:
        configure_logging()

    # Convert string context to dictionary if needed
    if isinstance(context, str):
        context = {"message": context}

    # Format the error with context
    error_info = format_error(error, context, include_traceback)

    # Log each component of the error separately
    logger.log(log_level, f"Error: {error_info['message']}")
    
    if context:
        logger.log(log_level, f"Context: {context}")
    
    if include_traceback and 'traceback' in error_info:
        logger.log(log_level, f"Traceback:\n{error_info['traceback']}")


# Alias functions with default logging methods
log_section = logger.info
log_key_value = logger.info
log_value = logger.info
log_dict = log_key_value
log_error = log_advanced_error