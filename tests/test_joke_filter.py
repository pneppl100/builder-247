"""
Test suite for Joke Filtering Logic
"""

import pytest
from src.joke_filter import filter_jokes

def test_filter_jokes_empty_input():
    """Test filtering an empty list of jokes"""
    assert filter_jokes([]) == []

def test_filter_jokes_max_length():
    """Test filtering jokes by maximum length"""
    jokes = [
        {'text': 'Short joke', 'tags': ['fun']},
        {'text': 'This is a very long joke that exceeds the maximum length limit', 'tags': ['fun']}
    ]
    filtered = filter_jokes(jokes, max_length=20)
    assert len(filtered) == 1
    assert filtered[0]['text'] == 'Short joke'

def test_filter_jokes_offensive_words():
    """Test filtering jokes with offensive words"""
    jokes = [
        {'text': 'A nice clean joke', 'tags': ['fun']},
        {'text': 'A joke with a BAD word in it', 'tags': ['adult']},
        {'text': 'Another joke with STUPID language', 'tags': ['humor']}
    ]
    filtered = filter_jokes(jokes, offensive_words=['bad', 'stupid'])
    assert len(filtered) == 1
    assert filtered[0]['text'] == 'A nice clean joke'

def test_filter_jokes_offensive_words_case_insensitive():
    """Test offensive word filtering is case-insensitive"""
    jokes = [
        {'text': 'A nice clean joke', 'tags': ['fun']},
        {'text': 'A joke with a BAD word in it', 'tags': ['adult']},
        {'text': 'Another joke with STUPID language', 'tags': ['humor']}
    ]
    filtered = filter_jokes(jokes, offensive_words=['Bad', 'Stupid'])
    assert len(filtered) == 1
    assert filtered[0]['text'] == 'A nice clean joke'

def test_filter_jokes_tags():
    """Test filtering jokes by tags"""
    jokes = [
        {'text': 'Science joke', 'tags': ['science']},
        {'text': 'Math joke', 'tags': ['math']},
        {'text': 'Programming joke', 'tags': ['tech']}
    ]
    filtered = filter_jokes(jokes, tags=['science', 'math'])
    assert len(filtered) == 2
    assert {joke['text'] for joke in filtered} == {'Science joke', 'Math joke'}

def test_filter_jokes_multiple_criteria():
    """Test filtering jokes with multiple criteria"""
    jokes = [
        {'text': 'Short science joke', 'tags': ['science']},
        {'text': 'Long offensive science joke with bad language', 'tags': ['science']},
        {'text': 'Very long joke that is not appropriate', 'tags': ['humor']},
        {'text': 'Clean tech joke', 'tags': ['tech']}
    ]
    filtered = filter_jokes(
        jokes, 
        max_length=20, 
        offensive_words=['bad', 'offensive'], 
        tags=['science', 'tech']
    )
    # Only the 'Short science joke' meets all criteria
    assert len(filtered) == 1
    assert filtered[0]['text'] == 'Short science joke'

def test_filter_jokes_no_matching_criteria():
    """Test filtering with no matching jokes"""
    jokes = [
        {'text': 'Long joke', 'tags': ['humor']},
        {'text': 'Offensive joke', 'tags': ['adult']}
    ]
    filtered = filter_jokes(
        jokes, 
        max_length=5, 
        offensive_words=['offensive'], 
        tags=['science']
    )
    assert filtered == []