"""
This file contains functions for reading PDF files.
"""

import pdfplumber
from gpt_pdf_organizer.utils.tokenizer import first_words_within_k_tokens

def read_pdf_page(pdf_path: str, page_index: int) -> str:
    """
    Iterate over the pages of a PDF file and yield the text of each page.
    """

    with pdfplumber.open(pdf_path) as pdf:
        if page_index >= len(pdf.pages):
            return None

        text = pdf.pages[page_index].extract_text()
        return text

