"""Advanced error handling utilities for the agent framework."""

from typing import Optional, Dict, Any
import traceback
import sys


class PrometheusError(Exception):
    """Base custom exception for the Prometheus framework."""

    def __init__(self, message: str, context: Optional[Dict[str, Any]] = None):
        """
        Initialize a Prometheus error with context.

        Args:
            message: Error description
            context: Optional dictionary with additional error context
        """
        super().__init__(message)
        self.message = message
        self.context = context or {}
        
        # Capture traceback at initialization
        self.traceback = ''.join(traceback.format_stack()[:-1])

    def __str__(self):
        """Provide a detailed string representation of the error."""
        context_str = ", ".join(f"{k}={v}" for k, v in self.context.items())
        return f"{self.message} [Context: {context_str}]"


class ClientAPIError(PrometheusError):
    """Error for API calls with additional status code information."""

    def __init__(
        self,
        message: str,
        status_code: int = 500,
        context: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize a client API error.

        Args:
            message: Error description
            status_code: HTTP status code
            context: Optional error context
        """
        super().__init__(message, context)
        self.status_code = status_code


class ConfigurationError(PrometheusError):
    """Error related to configuration issues."""
    pass


class AuthenticationError(PrometheusError):
    """Error related to authentication or authorization."""
    pass


class NetworkError(PrometheusError):
    """Error related to network connectivity or communication."""
    pass


class ResourceError(PrometheusError):
    """Error related to resource allocation or management."""
    pass


def format_error(
    error: Exception,
    context: Optional[Dict[str, Any]] = None,
    include_traceback: bool = True
) -> Dict[str, Any]:
    """
    Format an error into a structured dictionary.

    Args:
        error: The exception to format
        context: Optional additional context
        include_traceback: Whether to include stack trace

    Returns:
        Structured error dictionary
    """
    error_dict = {
        "error_type": error.__class__.__name__,
        "message": str(error),
        "context": context or {}
    }

    if include_traceback:
        try:
            error_dict["traceback"] = traceback.format_exc()
        except Exception:
            error_dict["traceback"] = "Unable to capture traceback"

    return error_dict