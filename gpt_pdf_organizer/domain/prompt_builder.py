"""
This module contains the functions to build the prompt that will be sent to AI LLM.
"""

from gpt_pdf_organizer.domain.attribute import Attribute


def build_query_from_content(content: str) -> str:
    return (f"Based on the following text extract of the first pages of a PDF file, extract: "
            f"\n\n {content}\n\n, what is the its content type (Book, Article or Unknown)? "
            "In the case content type is known (is Book or Article), also retrieve the Author, the Year and the Title of the original PDF file."
            "If content type is Unknown retrieve 'null' for Author, Year and Title. Output the answer "
            f"in json dictionary format like this: {{ \"{Attribute.CONTENT_TYPE.name.lower()}\":" 
            f"\"{Attribute.CONTENT_TYPE.name}\", \"{Attribute.AUTHOR.name.lower()}\": "
            f"\"{Attribute.AUTHOR.name}\", \"{Attribute.YEAR.name.lower()}\": \"{Attribute.YEAR.name}\"," 
            f"\"{Attribute.TITLE.name.lower()}\": \"{Attribute.TITLE.name}\"}}. "
            f"The CONTENT_TYPE must be one of ['book', 'article', 'null' ], All properties must be 'null' if CONTENT_TYPE is 'null' (unknown).'")
