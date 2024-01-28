"""
Defines the interface for a PromptQuerier service that will abstract the AI backend
for the prompt query service.
"""

from abc import ABC, abstractmethod
from typing import Dict 
from typing import Tuple

class PromptQuerier(ABC):
    """
    Defines the interface for a PromptQuerier service that will abstract the AI backend
    for the prompt query service.
    """

    def __init__(self, **kwargs: Dict):
        """
        Initializes the PromptQuerier with the given arguments.

        Args:
            **kwargs (Dict): Additional arguments to pass to the AI backend.
        """
        self._kwargs = kwargs

    @abstractmethod
    def query(self, prompt: str, **kwargs: Dict) -> str:
        """
        Queries the AI backend with the given prompt and returns the result.

        Args:
            prompt (str): The prompt to query with.
            **kwargs (Dict): Additional arguments to pass to the AI backend query.

        Returns:
            str: The generated tokens.
        """

    @abstractmethod
    def clamp_text_by_tokens(self, text: str, max_tokens: int) -> Tuple[str, int]:
        """
        Extracts the first k tokens from the given text.

        Args:
            text (str): The text to extract the first k tokens from.
            max_tokens (int): The number of tokens to extract.

        Returns:
            a tuple containing the extracted text and the total number of tokens effectivelly used.
        """
