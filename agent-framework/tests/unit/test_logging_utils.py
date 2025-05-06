"""Unit tests for logging utilities."""

import logging
import pytest
from io import StringIO
from unittest.mock import patch
from prometheus_swarm.utils.logging import (
    configure_logging,
    log_advanced_error,
    logger
)


def test_configure_logging():
    """Test logging configuration."""
    configure_logging(log_level=logging.DEBUG)
    assert logger.level == logging.DEBUG


def test_log_advanced_error_with_string_context(capsys):
    """Test advanced error logging with string context."""
    try:
        raise ValueError("Test error")
    except ValueError as e:
        # Log with string context
        log_advanced_error(e, "Test context")
        
        # Capture output
        captured = capsys.readouterr()
        
        assert "Test error" in captured.err
        assert "Test context" in captured.err
        assert "Traceback" in captured.err


def test_log_advanced_error_with_dict_context(capsys):
    """Test advanced error logging with dictionary context."""
    try:
        raise RuntimeError("Complex error")
    except RuntimeError as e:
        # Log with dictionary context
        log_advanced_error(
            e, 
            {"module": "test_module", "function": "test_function"},
            include_traceback=False
        )
        
        # Capture output
        captured = capsys.readouterr()
        
        assert "Complex error" in captured.err
        assert "test_module" in captured.err
        assert "test_function" in captured.err