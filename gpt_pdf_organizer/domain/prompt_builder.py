"""
This module contains the functions to build the prompt that will be sent to AI LLM.
"""

from gpt_pdf_organizer.domain.attribute import Attribute

topics = {
    "Natural Sciences": [
        "Physics",
        "Chemistry",
        "Biology",
        "Earth Sciences"
    ],
    "Formal Sciences": [
        "Mathematics",
        "Computer Science",
        "Statistics"
    ],
    "Applied Sciences": [
        "Engineering",
        "Medicine",
        "Agriculture"
    ],
    "Social Sciences": [
        "Psychology",
        "Economics",
        "Sociology"
    ],
    "Interdisciplinary Fields": [
        "Environmental Science",
        "Biotechnology",
        "Neuroscience"
    ],
    "Humanities": [
        "Science and technology studies", 
        "History and philosophy of science", 
        "Digital humanities"
    ]
}

def build_query_from_content(content: str) -> str:
    return (f"Based on the following text extract of the first pages of a PDF file, extract: "
            f"\n\n {content}\n\n, what is the its content type (Book, Article or Unknown)? "
            "In the case content type is known, also retrieve the Author, the Year and the Title of the original PDF file."
            f"Also provide one main topic and one subtopic that the PDF is about, from the given table of topics: {topics}, or 'null' if it cannot be infered."
            f"Output the answer in json dictionary format like this: "
            f"{{ \"{Attribute.CONTENT_TYPE.name.lower()}\":"
            f"\"{Attribute.CONTENT_TYPE.name}\", \"{Attribute.AUTHOR.name.lower()}\": "
            f"\"{Attribute.AUTHOR.name}\", \"{Attribute.YEAR.name.lower()}\": \"{Attribute.YEAR.name}\","
            f"\"{Attribute.TITLE.name.lower()}\": \"{Attribute.TITLE.name}\"}}. "
            f"\"{Attribute.TOPIC.name.lower()}\": \"{Attribute.TOPIC.name}\"}}. "
            f"\"{Attribute.SUB_TOPIC.name.lower()}\": \"{Attribute.SUB_TOPIC.name}\"}}. "
            "The CONTENT_TYPE must be one of ['book', 'article', 'null' ], Any property must be 'null' if cannot be deduced."
            )
