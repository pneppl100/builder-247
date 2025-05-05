"""Tool definitions for various command executions."""

from typing import List, Dict, Any
from .implementations import dad_joke_handler

TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "dad_joke_handler",
            "description": "Retrieves a random dad joke from an online API",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }
]

TOOL_IMPLEMENTATIONS = {
    "dad_joke_handler": dad_joke_handler
}