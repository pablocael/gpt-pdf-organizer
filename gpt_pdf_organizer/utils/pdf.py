"""
This file contains functions for reading PDF files.
"""

import pdfplumber
from gpt_pdf_organizer.utils.tokenizer import first_words_within_k_tokens

def read_first_k_tokens_from_pdf(pdf_path: str, k: int):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        page_index = 0
        total_tokens = 0
        current_text = ""
        while True:
            page = pdf.pages[page_index]
            text = page.extract_text()
            text, token_count = first_words_within_k_tokens(text, k - total_tokens)
            current_text += text
            total_tokens += token_count

            if total_tokens >= k:
                break

            page_index += 1

    # Split text into words and get the first N words
    return current_text

