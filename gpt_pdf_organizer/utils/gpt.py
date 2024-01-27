"""
This file contains the functions to query the GPT chatbot.
"""

import openai
from gpt_pdf_organizer.utils.config import GPT_MODEL_NAME
from gpt_pdf_organizer.utils.config import MAX_NUM_TOKENS

def build_query_from_content(content: str) -> str:
    return f"Based on this text extract of the first {MAX_NUM_TOKENS} words of this PDF, what is the likely content type of this PDF, a Book, an Article or Other? If its a book, also answer the year of publication, otherwise the year should be 'Unknown'. Answer exactly one of the in the format (CONTENT_TYPE, YEAR, TITLE). The CONTENT_TYPE is one of (Book, Article or Other). Extract: '{content}'"

def query_chatgpt(prompt):

    client = openai.OpenAI()

    response = client.chat.completions.create(
        model=GPT_MODEL_NAME,  # or the latest available model
        max_tokens=MAX_NUM_TOKENS,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": prompt},
        ]
    )

    return response.choices[0].message
