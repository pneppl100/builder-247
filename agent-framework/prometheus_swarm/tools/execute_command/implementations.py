"""Implementations for command execution tools."""

import requests
from typing import Dict, Any


def dad_joke_handler() -> Dict[str, Any]:
    """
    Retrieve a random dad joke from the icanhazdadjoke API.

    Returns:
        Dict with joke details: {'joke': str, 'status': int}
    """
    try:
        headers = {
            'Accept': 'application/json',
            'User-Agent': 'Prometheus Swarm (github.com/yourusername/repository)'
        }
        response = requests.get('https://icanhazdadjoke.com/', headers=headers)
        response.raise_for_status()
        joke_data = response.json()
        return {
            'joke': joke_data['joke'],
            'status': response.status_code
        }
    except requests.RequestException as e:
        return {
            'joke': f'Failed to fetch dad joke: {str(e)}',
            'status': 500
        }