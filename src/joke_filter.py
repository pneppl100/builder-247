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

    filtered_jokes = []

    for joke in jokes:
        # Check length
        if max_length is not None and len(joke.get('text', '')) > max_length:
            continue

        # Check offensive words
        if offensive_words_lower and any(
            word in joke.get('text', '').lower() 
            for word in offensive_words_lower
        ):
            continue

        # Check tags
        if tags and not any(tag in joke.get('tags', []) for tag in tags):
            continue

        filtered_jokes.append(joke)

    return filtered_jokes