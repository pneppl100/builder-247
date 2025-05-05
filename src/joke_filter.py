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

    filtered_jokes = []

    for joke in jokes:
        # Initialize flags for each criterion
        meets_length_criteria = True
        meets_offensive_criteria = True
        meets_tag_criteria = True

        # Check max length
        if max_length is not None:
            meets_length_criteria = len(joke.get('text', '')) <= max_length

        # Check offensive words
        if offensive_words:
            offensive_words_lower = [word.lower() for word in offensive_words]
            meets_offensive_criteria = not any(
                word in joke.get('text', '').lower() 
                for word in offensive_words_lower
            )

        # Check tags
        if tags:
            meets_tag_criteria = any(tag in joke.get('tags', []) for tag in tags)

        # Add joke only if it meets ALL specified criteria
        if meets_length_criteria and meets_offensive_criteria and meets_tag_criteria:
            filtered_jokes.append(joke)

    return filtered_jokes