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


def test_log_advanced_error_with_string_context():
    """Test advanced error logging with string context."""
    with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
        try:
            raise ValueError("Test error")
        except ValueError as e:
            # Log with string context
            log_advanced_error(e, "Test context")
            log_output = mock_stdout.getvalue()
            
            assert "Test error" in log_output
            assert "Context" in log_output
            assert "Traceback" in log_output


def test_log_advanced_error_with_dict_context():
    """Test advanced error logging with dictionary context."""
    with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
        try:
            raise RuntimeError("Complex error")
        except RuntimeError as e:
            # Log with dictionary context
            log_advanced_error(
                e, 
                {"module": "test_module", "function": "test_function"},
                include_traceback=False
            )
            log_output = mock_stdout.getvalue()
            
            assert "Complex error" in log_output
            assert "Context" in log_output