"""
This file contains the functions for tokenizing the text and selecting the first words within a token limit.
"""

import tiktoken

def first_words_within_k_tokens(text: str, k: int, llm_model_name: str):

    # Tokenize the text
    word_count = 0
    token_count = 0

    words = text.split()
    encoder = tiktoken.encoding_for_model(llm_model_name)

    for i, word in enumerate(words):
        # Count the tokens for the current word

        word_tokens = len(encoder.encode((word)))

        # Check if adding this word exceeds the token limit
        if token_count + word_tokens > k:
            break

        # Add the word's tokens to the total count and increment word count
        token_count += word_tokens
        word_count += 1

    # Join the words that fit within the token and word limits
    selected_text = ' '.join(words[:word_count])
    return selected_text, token_count
