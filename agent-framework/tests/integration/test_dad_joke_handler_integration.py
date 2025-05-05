"""Integration tests for Dad Joke Command Handler."""

import os
import pytest
import requests_mock
from prometheus_swarm.clients.anthropic_client import AnthropicClient
from prometheus_swarm.tools.execute_command.definitions import TOOL_DEFINITIONS
from prometheus_swarm.tools.execute_command.implementations import dad_joke_handler
from typing import Any, Dict


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

    # Mock the external API request
    with requests_mock.Mocker() as mocker:
        mocker.get('https://icanhazdadjoke.com/', json={
            'joke': 'Why don\'t scientists trust atoms? Because they make up everything!',
            'id': 'abcdef123',
            'status': 200
        }, headers={'Content-Type': 'application/json'})

        # Request a dad joke
        result: Dict[str, Any] = client.send_message(
            "Tell me a dad joke",
            tool_choice={"type": "required_any"},
        )

        # Validate the response type and general structure
        assert isinstance(result, dict), "Result should be a dictionary"
        assert "content" in result, "Result should have a 'content' key"
        assert isinstance(result["content"], list), "Content should be a list"

        # Verify at least one tool use in the content
        tool_calls = [block for block in result["content"] if block.get("type") == "tool_call"]
        assert len(tool_calls) > 0, "Should have at least one tool call"

        # Find the dad joke tool call
        dad_joke_calls = [call for call in tool_calls if call.get("tool_call", {}).get("name") == "dad_joke_handler"]
        assert len(dad_joke_calls) > 0, "Should have a dad joke tool call"

        tool_call = dad_joke_calls[0]["tool_call"]
        tool_use_id = tool_call.get("id")
        assert tool_use_id is not None, "Tool call should have an ID"

        # Simulate tool execution in a way compatible with the client's implementation
        mock_tool_use = type('MockToolUse', (), {
            'id': tool_use_id, 
            'name': 'dad_joke_handler'
        })
        
        # Attempt to execute the tool
        joke_data = client.execute_tool(mock_tool_use)
        
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
            tool_use_id=tool_use_id,
            conversation_id=result.get("conversation_id"),
        )

        # Verify response is a dictionary with expected structure
        assert isinstance(response, dict), "Response should be a dictionary"
        assert "content" in response, "Response should have a 'content' key"
        assert "role" in response, "Response should have a 'role' key"
        assert response["role"] == "assistant", "Response role should be 'assistant'"