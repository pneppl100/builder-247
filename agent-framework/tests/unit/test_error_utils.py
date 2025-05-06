"""Unit tests for error handling utilities."""

import pytest
from prometheus_swarm.utils.errors import (
    PrometheusError,
    ClientAPIError,
    ConfigurationError,
    format_error
)


def test_prometheus_error():
    """Test the base PrometheusError class."""
    context = {"module": "test", "action": "validation"}
    error = PrometheusError("Test error", context)

    assert str(error) == "Test error [Context: module=test, action=validation]"
    assert error.context == context
    assert "test_error_utils.py" in error.traceback


def test_client_api_error():
    """Test the ClientAPIError class."""
    context = {"endpoint": "/api/test", "method": "GET"}
    error = ClientAPIError("API request failed", status_code=400, context=context)

    assert error.status_code == 400
    assert "API request failed" in str(error)
    assert "endpoint=/api/test" in str(error)


def test_configuration_error():
    """Test the ConfigurationError class inheritance."""
    with pytest.raises(PrometheusError):
        raise ConfigurationError("Missing configuration", {"key": "missing_api_key"})


def test_format_error():
    """Test error formatting utility."""
    try:
        raise ValueError("Something went wrong")
    except ValueError as e:
        formatted_error = format_error(e, {"source": "test_module"})

    assert formatted_error["error_type"] == "ValueError"
    assert formatted_error["message"] == "Something went wrong"
    assert formatted_error["context"]["source"] == "test_module"
    assert "traceback" in formatted_error