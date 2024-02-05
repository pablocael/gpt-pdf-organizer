"""
This file contains the functions to query the GPT chatbot.
"""

import tiktoken
import openai
from gpt_pdf_organizer.service.prompt_querier import PromptQuerier
from gpt_pdf_organizer.utils.tokenizer import first_words_within_k_tokens
from typing import Dict
from typing import Tuple


class GPTPromptQuerier(PromptQuerier):
    """
    Defines the interface for a PromptQuerier service that will abstract the AI backend
    for the prompt query service.
    """

    def __init__(self, config: Dict):
        """
        Initializes the PromptQuerier with the given arguments.

        Args:
            **kwargs (Dict): Additional arguments to pass to the AI backend.
        """
        self._config = config

    def query(self, prompt: str, **kwargs) -> str:
        """
        Queries the AI backend with the given prompt and returns the result.

        Args:
            prompt (str): The prompt to query with.
            max_tokens (int): The maximum number of tokens to generate.
            **kwargs (Dict): Additional arguments to pass to the AI backend query.

        Returns:
            str: The generated tokens.
        """
        api_key = self._get_config("api_key")
        if not api_key:
            raise ValueError("API key must be specified")

        max_tokens = self._get_config("max_tokens")
        model_name = self._get_config("model_name")

        openai.api_key = api_key
        client = openai.OpenAI()

        response = client.chat.completions.create(
            model=model_name,  # or the latest available model
            max_tokens=max_tokens,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": prompt},
            ]
        )

        return response.choices[0].message.content

    def clamp_text_by_tokens(self, text: str, max_tokens: int) -> Tuple[str, int]:
        """
        Extracts the first k tokens from the given text.

        Args:
            text (str): The text to extract the first k tokens from.
            max_tokens (int): The number of tokens to extract.

        Returns:
            a tuple containing the extracted text and the total number of tokens effectivelly used.
        """

        # Tokenize the text
        word_count = 0
        token_count = 0

        words = text.split()
        encoder = tiktoken.encoding_for_model(self._get_config("model_name"))

        for i, word in enumerate(words):
            # Count the tokens for the current word

            word_tokens = len(encoder.encode((word)))

            # Check if adding this word exceeds the token limit
            if token_count + word_tokens > max_tokens:
                break

            # Add the word's tokens to the total count and increment word count
            token_count += word_tokens
            word_count += 1

        # Join the words that fit within the token and word limits
        selected_text = ' '.join(words[:word_count])
        return selected_text, token_count

    def _get_config(self, key):
        """
        Gets the config value for the given key.
        Args:
            key (str): The key to get the config value for.

        Returns:
            str: The config value.
        """
        return self._config.get(key)
