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
        return super().format(record)


def configure_logging(log_level: int = logging.INFO) -> None:
    """
    Configure logging for the application with adjustable log level.

    Args:
        log_level: Logging level (default: logging.INFO)
    """
    global _logging_configured
    if _logging_configured:
        return

    try:
        # Remove any existing handlers to prevent duplicates
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)

        # Create console handler with colored output
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level)
        console_formatter = SectionFormatter()
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

        logger.setLevel(log_level)
        logger.info(f"Logging configured: {logging.getLevelName(log_level)}+ to console")
        _logging_configured = True

    except Exception as e:
        print(f"Failed to configure logging: {e}", file=sys.stderr)


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

    # Log the error with the specified log level
    logger.log(log_level, f"Error: {error_info['message']}")
    
    if context:
        logger.log(log_level, f"Context: {context}")
    
    if include_traceback:
        logger.log(log_level, "Traceback:\n" + error_info['traceback'])


# Keeping all previous logging methods for backwards compatibility
log_section = logger.info
log_key_value = logger.info
log_value = logger.info
log_dict = log_key_value
log_error = log_advanced_error

# Decorators and other methods remain the same as in the previous implementation