"""Integration tests for Dad Joke Command Handler."""

import os
import pytest
from prometheus_swarm.clients.anthropic_client import AnthropicClient
from anthropic.types import Message
from prometheus_swarm.tools.execute_command.definitions import TOOL_DEFINITIONS
from prometheus_swarm.tools.execute_command.implementations import dad_joke_handler


@pytest.fixture(autouse=True)
def setup_environment():
    """Set up environment variables and client before each test."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        pytest.skip("ANTHROPIC_API_KEY environment variable not set")
    client = AnthropicClient(api_key=api_key)
    tools_config = next(tool for tool in TOOL_DEFINITIONS if tool['function']['name'] == 'dad_joke_handler')
    client.tools = {
        "dad_joke_handler": {
            "function": dad_joke_handler,
            "name": tools_config['function']['name'],
            "description": tools_config['function']['description'],
            "parameters": tools_config['function']['parameters']
        }
    }
    return client


def test_dad_joke_handler(setup_environment):
    """Test Dad Joke Command Handler integration."""
    client = setup_environment

    # Request a dad joke
    message = client.send_message(
        "Tell me a dad joke",
        tool_choice={"type": "required_any"},
    )

    assert isinstance(message, Message)
    assert message.stop_reason == "tool_use"
    tool_use = next(block for block in message.content if block.type == "tool_use")
    assert tool_use.name == "dad_joke_handler"

    # Execute tool and get response
    result = client.execute_tool(tool_use)
    joke_data = result[0]  # Assuming the result is a dictionary
    
    # Validate joke response
    assert isinstance(joke_data, dict)
    assert 'joke' in joke_data, "Response should contain 'joke' key"
    assert 'status' in joke_data, "Response should contain 'status' key"
    assert joke_data['status'] == 200, "API request should be successful"
    assert isinstance(joke_data['joke'], str), "Joke should be a string"
    assert len(joke_data['joke']) > 0, "Joke should not be empty"

    # Send a response based on the joke
    response = client.send_message(
        tool_response=str(joke_data),
        tool_use_id=tool_use.id,
        conversation_id=message.conversation_id,
    )

    assert isinstance(response, Message)
    assert all(block.type == "text" for block in response.content)