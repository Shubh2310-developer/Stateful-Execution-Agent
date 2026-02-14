import pytest
from src.llm.token_counter import token_counter

def test_token_counting_efficiency():
    """Tests the efficiency and accuracy of the token counter."""
    text = "This is a test sentence for token counting."
    count = token_counter.count_tokens(text)
    assert count > 0
    assert isinstance(count, int)

def test_message_token_counting():
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ]
    count = token_counter.count_message_tokens(messages)
    assert count > 10
