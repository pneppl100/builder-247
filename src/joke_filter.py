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

    filtered_jokes = jokes.copy()

    # Filter by max length
    if max_length is not None:
        filtered_jokes = [
            joke for joke in filtered_jokes 
            if len(joke.get('text', '')) <= max_length
        ]

    # Filter by offensive words
    if offensive_words:
        # Convert offensive words to lowercase for case-insensitive matching
        offensive_words = [word.lower() for word in offensive_words]
        filtered_jokes = [
            joke for joke in filtered_jokes
            if not any(
                word in joke.get('text', '').lower() 
                for word in offensive_words
            )
        ]

    # Filter by tags
    if tags:
        filtered_jokes = [
            joke for joke in filtered_jokes
            if any(tag in joke.get('tags', []) for tag in tags)
        ]

    return filtered_jokes