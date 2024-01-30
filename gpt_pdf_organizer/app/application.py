"""
The main application use case class.
"""

import os
import json
from typing import Dict
from typing import List
from typing import Optional

from gpt_pdf_organizer.service.prompt_querier import PromptQuerier
from gpt_pdf_organizer.domain.organizing_fields import OrganizingFields
from gpt_pdf_organizer.utils.file import read_files_from_path
from gpt_pdf_organizer.domain.prompt_builder import build_query_from_content
from gpt_pdf_organizer.utils.pdf import read_pdf_page
from gpt_pdf_organizer.utils.config import Config

import logging

logger = logging.getLogger(__name__)

class Application:

    def __init__(self, config: Config, prompt_querier: PromptQuerier, subfolders_from_attributes: Optional[List[OrganizingFields]] = None,
                 filenames_from_attributes: Optional[List[OrganizingFields]] = None):
        """
        Initialize the application.
        """
        self.config = config
        self.prompt_querier = prompt_querier

        self.subfolders_from_attributes = subfolders_from_attributes
        if self.subfolders_from_attributes is None:
            self.subfolders_from_attributes = [
                OrganizingFields.CONTENT_TYPE
            ]

        self.filenames_from_attributes = filenames_from_attributes
        if self.filenames_from_attributes is None:
            self.filenames_from_attributes = [
                OrganizingFields.TITLE
            ]

    def organize(self, input_path: str, output_dir: str):
        """
        Run the application.
        """

        self._initialize_output_dir(output_dir=output_dir)

        files = read_files_from_path(input_path, "pdf")
        logger.info("processing %d files from folder %s ...", (len(files), input_path))

        for file in files:
            logger.info("processing file %s ...", file)
            content = self._read_first_k_tokens_from_pdf(
                pdf_path=file, k=MAX_NUM_TOKENS)
            logger.debug("extracted content is content: %s", content)
            prompt = build_query_from_content(content=content)
            response = self.prompt_querier.query(prompt)

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
        if os.path.exists(output_dir) and len(os.listdir(output_dir)) > 0:
            raise ValueError(
                "Output directory already exists but is not empty, please specify a non-existing or empty directory")

        os.makedirs(output_dir, exist_ok=True)

    def build_filename_from_attribute_values(self, attribute_values: Dict[str, str]) -> str:
        """
        Build a filename from the given attributes.
        """
        filename = ""
        for i, attribute in enumerate(self.filenames_from_attributes):

            filename += attribute_values[attribute.name.lower()]
            if i < len(self.filenames_from_attributes) - 1:
                filename += ATTRIBUTES_SEPARATOR

        return filename

    def build_output_dir_from_attribute_values(self, attribute_values: Dict[str, str]) -> str:
        """
        Build an output directory from the given attributes.
        """
        output_dir = ""
        for i, attribute in enumerate(self.subfolders_from_attributes):
            output_dir = os.join(output_dir, attribute_values[attribute.name.lower()])

        return output_dir
