"""
The main application use case class.
"""

from typing import List
from typing import Optional

from gpt_pdf_organizer.service.prompt_querier import PromptQuerier
from gpt_pdf_organizer.domain.organizing_fields import OrganizingFields
from gpt_pdf_organizer.utils.file import read_files_from_path
from gpt_pdf_organizer.domain.prompt_builder import build_query_from_content
from gpt_pdf_organizer.utils.pdf import read_pdf_page 
from gpt_pdf_organizer.utils.config import MAX_NUM_TOKENS


class Application:

    def __init__(self, prompt_querier: PromptQuerier, organize_by_fields: Optional[List[OrganizingFields]] = None):
        """
        Initialize the application.
        """
        self.prompt_querier = prompt_querier

        self.organize_by_fields = organize_by_fields
        if self.organize_by_fields is None:
            self.organize_by_fields = [
                OrganizingFields.CONTENT_TYPE
            ]

    def organize(self, input_path: str, output_dir: str):
        """
        Run the application.
        """
        files = read_files_from_path(input_path, "pdf")

        for file in files:
            content = self._read_first_k_tokens_from_pdf(
                pdf_path=file, k=MAX_NUM_TOKENS)
            prompt = build_query_from_content(content=content)
            response = self.prompt_querier.query(prompt)
            print(response)

    def _read_first_k_tokens_from_pdf(self, pdf_path: str, k: int) -> str:
        """
        Read the first k tokens from the given PDF file.
        """
        current_text = ""
        current_page = 0
        total_tokens_read = 0
        while True:
            text = read_pdf_page(pdf_path=pdf_path,
                                 page_index=current_page)
            text, num_tokens_read = self.prompt_querier.clamp_text_by_tokens(
                text=text, max_tokens=k - total_tokens_read)
            total_tokens_read += num_tokens_read
            current_text += text

            if total_tokens_read >= k:
                break

            current_page += 1

        return current_text

    def _initialize_output_dir(self, output_dir: str):
        """
        Initialize the output directory.
        """
        if not os.path.exists(output_dir):
            os.makedirs(os.path.join(output_dir, "pdfs"))
