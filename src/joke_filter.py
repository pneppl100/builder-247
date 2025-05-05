"""
Joke Filtering Logic Module

This module provides functionality to filter jokes based on various criteria.
"""

def filter_jokes(jokes, max_length=None, offensive_words=None, tags=None):
    """
    Filter a list of jokes based on multiple criteria.

    Args:
        jokes (list): A list of joke dictionaries.
        max_length (int, optional): Maximum length of joke text. Defaults to None.
        offensive_words (list, optional): List of offensive words to filter. Defaults to None.
        tags (list, optional): List of allowed tags. Defaults to None.

    Returns:
        list: Filtered list of jokes that meet ALL specified criteria.
    """
    if not jokes:
        return []

    # Convert optional parameters to empty lists if None
    offensive_words = offensive_words or []
    tags = tags or []

    # Convert offensive words to lowercase for case-insensitive matching
    offensive_words_lower = [word.lower() for word in offensive_words]

    # Filter jokes that match ALL criteria
    filtered_jokes = [
        joke for joke in jokes
        if (max_length is None or len(joke.get('text', '')) <= max_length) and
           (not offensive_words_lower or 
            not any(word in joke.get('text', '').lower() for word in offensive_words_lower)) and
           (not tags or any(tag in joke.get('tags', []) for tag in tags))
    ]

    return filtered_jokes